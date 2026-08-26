import React, { createContext, useContext, useState, useEffect } from 'react';

const RouterContext = createContext({
  path: window.location.pathname,
  navigate: () => {},
  params: {}
});

export function BrowserRouter({ children }) {
  const [path, setPath] = useState(window.location.pathname || '/');

  useEffect(() => {
    const handlePop = () => {
      setPath(window.location.pathname || '/');
    };
    window.addEventListener('popstate', handlePop);
    return () => window.removeEventListener('popstate', handlePop);
  }, []);

  const navigate = (newPath, options = {}) => {
    if (options.replace) {
      window.history.replaceState({}, '', newPath);
    } else {
      window.history.pushState({}, '', newPath);
    }
    setPath(newPath);
    window.scrollTo(0, 0);
  };

  return (
    <RouterContext.Provider value={{ path, navigate }}>
      {children}
    </RouterContext.Provider>
  );
}

export function useNavigate() {
  const { navigate } = useContext(RouterContext);
  return navigate;
}

export function useLocation() {
  const { path } = useContext(RouterContext);
  return { pathname: path };
}

export function useParams() {
  const { path } = useContext(RouterContext);
  // Match :id from /inspections/:id or /products/:id
  const parts = path.split('/').filter(Boolean);
  if (parts.length >= 2) {
    return { id: parts[1] };
  }
  return {};
}

export function Routes({ children }) {
  const { path } = useContext(RouterContext);

  let matchedElement = null;
  React.Children.forEach(children, (child) => {
    if (!React.isValidElement(child) || matchedElement) return;

    const routePath = child.props.path;
    if (routePath === '*') {
      matchedElement = child.props.element;
      return;
    }

    if (routePath === '/*') {
      matchedElement = child.props.element;
      return;
    }

    if (routePath === path) {
      matchedElement = child.props.element;
      return;
    }

    // Dynamic param matching like /inspections/:id
    if (routePath && routePath.includes(':id')) {
      const pattern = new RegExp('^' + routePath.replace(':id', '([^/]+)') + '$');
      if (pattern.test(path)) {
        matchedElement = child.props.element;
      }
    }
  });

  return matchedElement || null;
}

export function Route({ path, element }) {
  return element;
}

export function Link({ to, children, className = '', ...props }) {
  const { navigate } = useContext(RouterContext);

  const handleClick = (e) => {
    e.preventDefault();
    navigate(to);
  };

  return (
    <a href={to} onClick={handleClick} className={className} {...props}>
      {children}
    </a>
  );
}

export function NavLink({ to, children, className, ...props }) {
  const { path, navigate } = useContext(RouterContext);
  const isActive = path === to || (to !== '/' && path.startsWith(to));

  const computedClass = typeof className === 'function' ? className({ isActive }) : className;

  const handleClick = (e) => {
    e.preventDefault();
    navigate(to);
  };

  return (
    <a href={to} onClick={handleClick} className={computedClass} {...props}>
      {children}
    </a>
  );
}

export function Navigate({ to, replace }) {
  const { navigate } = useContext(RouterContext);
  useEffect(() => {
    navigate(to, { replace });
  }, [to, replace, navigate]);

  return null;
}

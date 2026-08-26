import re
from typing import Dict, Any, List
from app.schemas.schemas import EcommerceVerificationRequest, EcommerceVerificationResponse, DiscrepancyItem

class EcommerceService:
    """
    Service to verify E-Commerce Digital Product Listings against Legal Metrology Rules
    and physical package declarations (Rule 6(11) & E-Commerce Guidelines).
    """

    @classmethod
    def verify_listing(cls, req: EcommerceVerificationRequest, package_data: Dict[str, Any] = None) -> EcommerceVerificationResponse:
        discrepancies: List[DiscrepancyItem] = []
        score = 100.0

        pkg_mrp = req.package_mrp or (package_data.get("mrp") if package_data else None)
        pkg_qty = req.package_net_quantity or (package_data.get("net_quantity") if package_data else None)
        pkg_mfg = req.package_manufacturer or (package_data.get("manufacturer") if package_data else None)

        # 1. Compare MRP
        if pkg_mrp is not None and req.listing_mrp:
            # Clean MRP strings if passed as numeric or text
            try:
                pkg_mrp_num = float(re.search(r"(\d+(?:\.\d+)?)", str(pkg_mrp)).group(1))
                list_mrp_num = float(req.listing_mrp)
                
                if list_mrp_num > pkg_mrp_num:
                    diff = list_mrp_num - pkg_mrp_num
                    discrepancies.append(DiscrepancyItem(
                        field="Maximum Retail Price (MRP)",
                        package_value=f"₹{pkg_mrp_num:.2f}",
                        listing_value=f"₹{list_mrp_num:.2f}",
                        issue_type="MRP_MISMATCH",
                        severity="CRITICAL",
                        legal_rule="Rule 6(11) & Rule 18(2), Legal Metrology (PC) Rules, 2011",
                        description=f"Online listing declares inflated MRP (₹{list_mrp_num:.2f}) compared to physical package MRP (₹{pkg_mrp_num:.2f}). Selling above package MRP or artificially inflating MRP is a strict violation under Section 36."
                    ))
                    score -= 40.0
                elif list_mrp_num < pkg_mrp_num:
                    discrepancies.append(DiscrepancyItem(
                        field="Maximum Retail Price (MRP)",
                        package_value=f"₹{pkg_mrp_num:.2f}",
                        listing_value=f"₹{list_mrp_num:.2f}",
                        issue_type="MRP_MISMATCH",
                        severity="MEDIUM",
                        legal_rule="Rule 6(11), Legal Metrology (PC) Rules, 2011",
                        description="Listing MRP differs from current batch physical package MRP. Verify if this belongs to an older manufacturing batch."
                    ))
                    score -= 15.0
            except Exception:
                pass

        # 2. Compare Net Quantity
        if pkg_qty and req.listing_net_quantity:
            pkg_q_str = str(pkg_qty).lower().replace(" ", "")
            list_q_str = str(req.listing_net_quantity).lower().replace(" ", "")
            if pkg_q_str != list_q_str:
                discrepancies.append(DiscrepancyItem(
                    field="Net Quantity",
                    package_value=str(pkg_qty),
                    listing_value=str(req.listing_net_quantity),
                    issue_type="QUANTITY_MISMATCH",
                    severity="HIGH",
                    legal_rule="Rule 6(1)(c) & Rule 6(11), Legal Metrology (PC) Rules, 2011",
                    description=f"Online listing claims net quantity '{req.listing_net_quantity}' while physical commodity contains '{pkg_qty}'. Misleading quantity declarations mislead consumers."
                ))
                score -= 30.0

        # 3. Country of Origin on Digital Platform
        if not req.listing_country_of_origin or len(req.listing_country_of_origin.strip()) < 2:
            discrepancies.append(DiscrepancyItem(
                field="Country of Origin",
                package_value="Declared on Package",
                listing_value="Missing on Marketplace Listing",
                issue_type="ORIGIN_MISMATCH",
                severity="HIGH",
                legal_rule="Legal Metrology E-Commerce Notification 2017 & Rule 6(10)",
                description="Digital e-commerce platforms must display Country of Origin prominently on product details page prior to purchase."
            ))
            score -= 20.0

        # 4. Manufacturer Details
        if not req.listing_manufacturer or len(req.listing_manufacturer.strip()) < 3:
            discrepancies.append(DiscrepancyItem(
                field="Manufacturer Details",
                package_value="Declared on Package",
                listing_value="Missing / Incomplete on Digital Listing",
                issue_type="MISSING_DECLARATION",
                severity="MEDIUM",
                legal_rule="Rule 6(1)(b) & E-Commerce Rules",
                description="Manufacturer and importer name/address must be disclosed on e-commerce listing."
            ))
            score -= 10.0

        score = max(0.0, min(100.0, round(score, 1)))

        if any(d.severity == "CRITICAL" for d in discrepancies) or score < 60.0:
            status = "HIGH_RISK"
            recommendation = "ISSUE NOTICE UNDER SECTION 36: Immediate inspection notice recommended to e-commerce marketplace entity and seller for MRP/Quantity violation."
        elif len(discrepancies) > 0:
            status = "MISMATCH_DETECTED"
            recommendation = "MANUAL VERIFICATION REQUIRED: Require seller to update digital listing to match physical packaging declarations."
        else:
            status = "PASS"
            recommendation = "COMPLIANT: Online listing declarations match physical package declarations."

        return EcommerceVerificationResponse(
            status=status,
            compliance_score=score,
            discrepancies=discrepancies,
            recommendation=recommendation
        )

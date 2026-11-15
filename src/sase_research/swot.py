"""Task 3: SWOT per vendor. Every point rests on a figure in data/ or a cited review signal."""

SWOT = {
    "Zscaler": {
        "S": [
            "Largest inline security cloud: 750B+ daily transactions across 200+ data centres",
            "ARR $3.77B (+25%); 785 customers above $1M ARR; net retention 115%",
            "Gartner Leader in both SSE (5th year) and SASE Platforms (first year)",
        ],
        "W": [
            "GAAP operating loss persists (-4.0% margin); stock pay $830M exceeds free cash flow",
            "85% of revenue flows through channel partners; top five = 31%",
            "Quote-only pricing at roughly $150-$300 per user per year for ZIA + ZPA",
        ],
        "O": [
            "AI security and non-seat products: metered ARR more than doubled in FY2026",
            "Asia Pacific revenue growing 23%, still only 15% of the mix",
            "Branch and SD-WAN replacement as access routers decline 25% Y/Y",
        ],
        "T": [
            "Palo Alto platform bundles: $450M of SASE displacements in FY2026",
            "Growth guided to slow from 25% to about 17% in FY2027",
            "Integration risk from four FY2026 acquisitions ($918M cash; goodwill nearly tripled)",
        ],
    },
    "Palo Alto Networks": {
        "S": [
            "Scale: Next-Gen Security ARR $9.1B, up 63%; RPO $21.2B",
            "One policy language across firewalls, SASE and SD-WAN",
            "Gartner Leader placed highest for Completeness of Vision",
        ],
        "W": [
            "Dual-unit licensing: per user plus per Mbps for remote networks",
            "Field benchmark of about $14-$22 per user per month before add-ons",
            "Lowest G2 rating of the five (4.3)",
        ],
        "O": [
            "Platformisation: target of 4,000+ platformised customers by FY2030",
            "Agentic traffic on its SASE platform rose 9x in nine months",
            "Converting its installed firewall base to Prisma Access",
        ],
        "T": [
            "SME buyers priced out; challengers win on simplicity",
            "FY2027 NGS ARR growth guided down to 22%-23%",
            "Integration load from recent acquisitions, including Chronosphere",
        ],
    },
    "Netskope": {
        "S": [
            "ARR $811M growing 31%; first full year of positive free cash flow",
            "Gartner SASE Leader, highest for Ability to Execute",
            "Top score in 3 of 5 Critical Capabilities use cases, including Sovereign SASE",
        ],
        "W": [
            "Deep GAAP losses: FY2026 operating margin -92% (IPO-related stock pay)",
            "Quote-only; renewals reported to carry 5%-10% annual escalators",
            "SD-WAN is younger than Cato's or Palo Alto's",
        ],
        "O": [
            "Sovereign-SASE demand as data-localisation rules spread",
            "AI gateway and agentic-broker products for GenAI traffic",
            "Lowest reported per-user medians among quote-only vendors ($50-$98)",
        ],
        "T": [
            "Public-market pressure to reach GAAP profitability",
            "Bundled platforms from Palo Alto and Zscaler",
            "Free-tier competition from Cloudflare at the low end",
        ],
    },
    "Cloudflare": {
        "S": [
            "Only vendor with published per-user pricing: free to 50 users, then $7/user/month",
            "Highest G2 rating among the five (4.6) and a Colombo PoP since 2017",
            "Company revenue up 39% to a $3B+ run-rate; net retention 122%",
        ],
        "W": [
            "Gartner Visionary, not Leader; about 400 enterprise SASE customers (2025 estimate)",
            "Reviewers cite a steep learning curve when combining products",
            "SD-WAN and DLP depth trail the leaders",
        ],
        "O": [
            "Land small firms free and expand as they grow past 50 users",
            "Added 158,000 paying customers in Q3 2026; partners can package managed SASE",
            "Privacy laws (Sri Lanka PDPA, India DPDP) push small firms to formal controls",
        ],
        "T": [
            "Enterprise buyers default to Leaders on Gartner shortlists",
            "Rising cost of revenue: gross margin fell to 71.2% in Q3 2026",
            "Leaders may launch SME tiers that copy the free-entry model",
        ],
    },
    "Cato Networks": {
        "S": [
            "Single-vendor SASE pioneer; Gartner Leader for the 3rd consecutive year",
            "Fast growth: ARR $415M+ up 42%; >4,000 enterprise customers",
            "Best ease-of-use score (G2 9.1/10); Gartner Peer Insights 4.7",
        ],
        "W": [
            "Per-site plus bandwidth pricing; reported as uncompetitive below ~50 users",
            "Private company with a fraction of Palo Alto's R&D budget",
            "Fewer integrations than the largest platforms",
        ],
        "O": [
            "Mid-market branch modernisation as access routers decline",
            "AI security via the Aim Security acquisition",
            "A possible IPO would fund regional expansion",
        ],
        "T": [
            "Price competition from Cloudflare at the bottom and bundles at the top",
            "IPO timing uncertainty",
            "Hardware socket model is heavy for single-office firms",
        ],
    },
}

ENTRANT = {
    "title": "Managed SASE for Sri Lankan SMEs (proposed entrant)",
    "S": [
        "Local presence, language and support hours that global vendors do not offer",
        "Can resell a free-to-start platform (Cloudflare One) with a local PoP",
        "Compliance-led pitch timed to PDPA from 1 Jan 2027",
    ],
    "W": [
        "No brand and no installed base",
        "Thin margins on resale unless services are bundled",
        "Small skilled team; key-person risk",
    ],
    "O": [
        "~650,000 seats at modal inputs; no published sizing of this segment found",
        "India DPDP substantive duties from 13 May 2027 open a second market",
        "12,650 cyber complaints to Sri Lanka CERT in 2025 raise awareness",
    ],
    "T": [
        "SME budgets are tight after the 2022 crisis",
        "Global vendors could sell direct or through telcos",
        "PDPA enforcement could slip, weakening urgency",
    ],
}

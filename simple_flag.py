# From your earlier analyze_output.py: "c(vFL)QrnvGl`KxTMJ~BE%pELAhR"
text = "c(vFL)QrnvGl`KxTMJ~BE%pELAhR"

# Find FL in the text
if "FL" in text:
    start = text.find("FL")
    # Try to extract until end or until non-printable
    flag_candidate = text[start:]
    print(f"Flag candidate: FLAG{{{flag_candidate[2:]}}}")  # Remove "FL"
    
    # Or if it already has { and }
    if "{" in flag_candidate and "}" in flag_candidate:
        print(f"Possible flag: {flag_candidate}")
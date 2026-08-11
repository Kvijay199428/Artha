def amount_in_words(amount: float) -> str:
    """Convert numeric amount to words (Indian numbering)."""
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_less_than_thousand(n):
        if n == 0:
            return ""
        elif n < 20:
            return ones[n]
        elif n < 100:
            return tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])
        else:
            return ones[n // 100] + " Hundred" + ("" if n % 100 == 0 else " and " + convert_less_than_thousand(n % 100))
    
    if amount == 0:
        return "Zero Rupees Only"
    
    rupees = int(amount)
    paise = round((amount - rupees) * 100)
    
    result = ""
    if rupees > 0:
        crore = rupees // 10000000
        lakh = (rupees // 100000) % 100
        thousand = (rupees // 1000) % 100
        remainder = rupees % 1000
        
        parts = []
        if crore > 0:
            parts.append(convert_less_than_thousand(crore) + " Crore")
        if lakh > 0:
            parts.append(convert_less_than_thousand(lakh) + " Lakh")
        if thousand > 0:
            parts.append(convert_less_than_thousand(thousand) + " Thousand")
        if remainder > 0:
            parts.append(convert_less_than_thousand(remainder))
        
        result = " ".join(parts) + " Rupees"
    
    if paise > 0:
        if result:
            result += " and "
        result += convert_less_than_thousand(paise) + " Paise"
    
    return result + " Only"
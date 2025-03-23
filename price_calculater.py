import json

base_prices = {
            "10-25cm": 50, 
            "25-30cm": 60, 
            "30-35cm": 70, 
            "35-40cm": 80,
            "41-45cm": 85, 
            "46-50cm": 90, 
            "51-55cm": 95, 
            "56-60cm": 100,
            "61-65cm": 105,
            "66-70cm": 110, 
            "71-75cm": 120, 
            "76-80cm": 130,
            "81-85cm": 140, 
            "86-90cm": 160
        }

def Aluminium_Doosletter_Price_calculator(letters, data):
    """
    Calculates the price of each letter based on given parameters.
    """
    try:
        data = json.loads(data)  # Parse JSON-formatted string
        thickness = int(data.get("thickness_pricing", 3))
        width_of_letter = int(data.get("width_of_letter", 6))
        colors = data.get("colors", [])

        

        thickness_price_adjustments = {3: 0, 5: 10, 8: 15, 20: 20}
        width_adjustment_per_cm = 2.5  
        extra_color_cost = 20 if len(colors) > 1 else 0

        prices = []
        for letter in letters:
            scaled_height = letter["scaled_height"]
            scaled_length = letter["scaled_length"]  # Fixed typo from scaled_length
            base_price = None

            for height_range, price in base_prices.items():
                min_h, max_h = map(lambda x: int(x.replace("cm", "")), height_range.split('-'))
                if min_h <= scaled_height <= max_h:
                    base_price = price
                    break

            if base_price is None:
                base_price = 160  # Default highest price if beyond 90cm

            width_adjustment = (abs(width_of_letter - 6) * width_adjustment_per_cm)

            final_price = base_price * (1 + (width_adjustment / 100))
            final_price += (base_price * (thickness_price_adjustments.get(thickness, 0) / 100))
            final_price += extra_color_cost

            prices.append({
                "letter": letter["letter"],
                "scaled_length": scaled_length,
                "scaled_height": scaled_height,
                "price": round(final_price, 2)
            })
        
        data = {
            "totalPrice" : sum(item["price"] for item in prices),
            "prices" : prices
        }
        return data
    except Exception as e:
        return {"error": str(e)}


def Profiel2_Price_calculator(letters, data):
    """
    Calculates the price of each letter based on given parameters.
    """
    try:
        data = json.loads(data)  
       
        width_of_letter = int(data.get("width_of_letter", 6))
        colors = data.get("colors", [])

        

        width_adjustment_per_cm = 2.5  
        extra_color_cost = 20 if len(colors) > 1 else 0

        prices = []
        for letter in letters:
            scaled_height = letter["scaled_height"]
            scaled_length = letter["scaled_length"]  # Fixed typo from scaled_length
            base_price = None

            for height_range, price in base_prices.items():
                min_h, max_h = map(lambda x: int(x.replace("cm", "")), height_range.split('-'))
                if min_h <= scaled_height <= max_h:
                    base_price = price
                    break

            if base_price is None:
                base_price = 160  # Default highest price if beyond 90cm

            width_adjustment = (abs(width_of_letter - 6) * width_adjustment_per_cm)

            final_price = base_price * (1 + (width_adjustment / 100))
            final_price += extra_color_cost

            prices.append({
                "letter": letter["letter"],
                "scaled_length": scaled_length,
                "scaled_height": scaled_height,
                "price": round(final_price, 2)
            })
        
        data = {
            "totalPrice" : sum(item["price"] for item in prices),
            "prices" : prices
        }
        return data
    except Exception as e:
        return {"error": str(e)}


def Profiel3_LUX_Price_calculator(letters, data):
    """
    Calculates the price of each letter based on given parameters.
    """
    try:
        data = json.loads(data)  # Parse JSON-formatted string
        plexi_size = int(data.get("plexi_size", 10))
        width_of_letter = int(data.get("width_of_letter", 6))
        colors = data.get("colors", [])

        plexi_size_adjustment = {10: 0, 20: 30, 30: 45}
        width_adjustment_per_cm = 2.5  
        extra_color_cost = 20 if len(colors) > 1 else 0

        prices = []
        for letter in letters:
            scaled_height = letter["scaled_height"]
            scaled_length = letter["scaled_length"]  # Fixed typo from scaled_length
            base_price = None

            for height_range, price in base_prices.items():
                min_h, max_h = map(lambda x: int(x.replace("cm", "")), height_range.split('-'))
                if min_h <= scaled_height <= max_h:
                    base_price = price
                    break

            if base_price is None:
                base_price = 160  # Default highest price if beyond 90cm

            width_adjustment = (abs(width_of_letter - 6) * width_adjustment_per_cm)

            final_price = base_price * (1 + (width_adjustment / 100))
            final_price += (base_price * (plexi_size_adjustment.get(plexi_size, 0) / 100))
            final_price += extra_color_cost

            prices.append({
                "letter": letter["letter"],
                "scaled_length": scaled_length,
                "scaled_height": scaled_height,
                "price": round(final_price, 2)
            })
        
        data = {
            "totalPrice" : sum(item["price"] for item in prices),
            "prices" : prices
        }
        return data
    except Exception as e:
        return {"error": str(e)}

def Profiel4_Price_calculator(letters, data):
    """
    Calculates the price of each letter based on given parameters.
    """
    try:
        data = json.loads(data)  # Parse JSON-formatted string
        plexi_size = int(data.get("plexi_size", 3))
        width_of_letter = int(data.get("width_of_letter", 6))
        colors = data.get("colors", [])

        plexi_size_adjustment = {3: 0, 5: 10, 10: 15}
        width_adjustment_per_cm = 2.5  
        extra_color_cost = 20 if len(colors) > 1 else 0

        prices = []
        for letter in letters:
            scaled_height = letter["scaled_height"]
            scaled_length = letter["scaled_length"]  # Fixed typo from scaled_length
            base_price = None

            for height_range, price in base_prices.items():
                min_h, max_h = map(lambda x: int(x.replace("cm", "")), height_range.split('-'))
                if min_h <= scaled_height <= max_h:
                    base_price = price
                    break

            if base_price is None:
                base_price = 160  # Default highest price if beyond 90cm

            width_adjustment = (abs(width_of_letter - 6) * width_adjustment_per_cm)

            final_price = base_price * (1 + (width_adjustment / 100))
            final_price += (base_price * (plexi_size_adjustment.get(plexi_size, 0) / 100))
            final_price += extra_color_cost

            prices.append({
                "letter": letter["letter"],
                "scaled_length": scaled_length,
                "scaled_height": scaled_height,
                "price": round(final_price, 2)
            })
        
        data = {
            "totalPrice" : sum(item["price"] for item in prices),
            "prices" : prices
        }
        return data
    except Exception as e:
        return {"error": str(e)}




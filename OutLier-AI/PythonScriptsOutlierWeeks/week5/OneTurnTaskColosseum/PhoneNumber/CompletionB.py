def locate_friend_phone(self, phone_no):
    try:
        # Remove any non-digit characters from the phone number
        clean_phone = ''.join(c for c in phone_no if c.isdigit())
        
        # Initialize the formatted phone number
        formatted_phone = ""
        
        # If the number already includes country code (like 972579090033)
        if len(clean_phone) == 12 and clean_phone.startswith('972'):
            formatted_phone = f"+{clean_phone}"
        # If the number is local format (like 579090033 or 0579090033)
        elif len(clean_phone) == 9:
            formatted_phone = f"+972{clean_phone}"
        elif len(clean_phone) == 10 and clean_phone.startswith('0'):
            # Remove leading 0 and add country code
            formatted_phone = f"+972{clean_phone[1:]}"
        elif len(clean_phone) == 10 and not clean_phone.startswith('0'):
            formatted_phone = f"+972{clean_phone}"
        
        # Ensure formatted_phone is ready before using it
        if formatted_phone:
            # Wait for the element to be selectable
            phone_no_element = self._driver.wait_to_click_element(
                XCUIElementTypeStaticTextName(formatted_phone)
            )
            return True if phone_no_element else False
        else:
            # Handle when formatted_phone is not ready (phone number isn't the expected length)
            return False
            
    except NoSuchElementException:
        return False

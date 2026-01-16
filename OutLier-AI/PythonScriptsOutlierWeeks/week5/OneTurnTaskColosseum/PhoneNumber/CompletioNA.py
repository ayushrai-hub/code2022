def locate_friend_phone(self, phone_no: str) -> bool:
    """
    Try to locate a phone number on the current screen.

    *  +97258090033  ->  +97258090033   (unchanged)
    *  0589090033    ->  058-909-0033   (old behaviour)
    *  589090033     ->  58-909-0033    (old behaviour)
    """
    try:
        # strip all white‑spaces
        phone_no = phone_no.replace(' ', '')

        # if the string starts with +NNN treat it as an international number
        if phone_no.startswith('+'):
            # keep only '+' and digits
            phone_no_xpath = ''.join(c for c in phone_no if c == '+' or c.isdigit())
        else:
            # local number – remove every non‑digit first
            phone_no = ''.join(c for c in phone_no if c.isdigit())

            phone_no_xpath = ""
            if len(phone_no) == 10:
                phone_no_xpath = f"{phone_no[:3]}-{phone_no[3:6]}-{phone_no[6:]}"
            elif len(phone_no) == 9:
                phone_no_xpath = f"{phone_no[:2]}-{phone_no[2:5]}-{phone_no[5:]}"
            elif len(phone_no) == 11:
                phone_no_xpath = f"{phone_no[:3]}-{phone_no[3:6]}-{phone_no[6:]}"
            elif len(phone_no) == 12:
                phone_no_xpath = f"{phone_no[:4]}-{phone_no[4:7]}-{phone_no[7:]}"

        # if nothing could be produced – abort
        if not phone_no_xpath:
            return False

        # look for the element
        elem = self._driver.wait_to_click_element(
            XCUIElementTypeStaticTextName(phone_no_xpath)
        )
        return elem is not None

    except NoSuchElementException:
        return False

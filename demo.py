from us_visa.logger import logging

logging.info("welcome to our custom log")



from us_visa.exception import us_visa_exception
import sys

try:
    a = 1/"e"

except Exception as error:
    raise us_visa_exception(error, sys) from error
import time
import random
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, InvalidArgumentException
from selenium.webdriver.common.by import By
import urllib.parse


def is_valid_url(url):
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to be validated.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class ScrapingError(Exception):
    """Custom exception for scraping errors."""


class InvalidURLException(ScrapingError):
    """Exception raised for invalid URL."""


class PageElementNotFoundError(ScrapingError):
    """Exception raised when a required page element is not found."""


class PageLoadError(ScrapingError):
    """Exception raised when there is an issue loading the page."""


class Job:
    """
    Represents a job posting with its title, company, description, and URL.
    """

    def __init__(self, title, company_name, description, url,  company_link, location):
        """
        Initialize a Job instance.

        Args:
            title (str): Title of the job.
            company_name (str): Company offering the job.
            description (str): Description of the job.
            url (str): URL of the job posting.
        """
        self.title = title
        self.company_name = company_name
        self.description = description
        self.url = url
        self.company_link = company_link
        self.location = location


    def __str__(self):
        """
        Return a formatted string representation of the Job instance.
        """
        return f"Title: {self.title}\nCompany: {self.company_name}\nDescription: {self.description}"

    def get_title(self):
        """
        Get the job title.

        Returns:
            str: The job title.
        """
        return self.title

    def get_company_name(self):
        """
        Get the name of the company offering the job.

        Returns:
            str: The company name.
        """
        return self.company_name

    def get_description(self):
        """
        Get the job description.

        Returns:
            str: The job description.
        """
        return self.description

    def get_url(self):
        """
        Get the URL of the job posting.

        Returns:
            str: The job posting URL.
        """
        return self.url

    def get_location(self):
        """
        Get the location of the company offering the job.

        Returns:
            str: The company name.
        """
        return self.location

    def get_company_link(self):
        """
        Get the link for the LinkedIn page of the company offering the job.

        Returns:
        str: The company name.
        """
        return self.company_link




def get_driver():
    """
    Initialize and return a headless Edge web driver.

    Returns:
        WebDriver: A Selenium web driver instance.
    """
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('headless')
    edge_options.add_argument("--incognito")
    return webdriver.Edge(options=edge_options)


def get_element(driver, element):
    """
    Find and return a web element using its XPath.

    Args:
        driver (WebDriver): The Selenium web driver.
        element (str): XPath of the element to find.

    Returns:
        WebElement: The found web element.
    """
    time.sleep(random.uniform(0.0, 0.3))
    return driver.find_element(By.XPATH, element)


def scraping_job_data(url):
    """
    Scrapes job information from a given URL.

    Args:
        url (str): The URL of the job posting on LinkedIn.

    Returns:
        Job or None: A Job instance representing job information (title, company, description) if successful,
        otherwise None.
    """
    driver = get_driver()
    try:
        if not is_valid_url(url):
            raise InvalidURLException("Invalid URL")

        # XPaths for extracting job title, company, and job description from the LinkedIn job page.
        title_tag = "//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open " \
                    "text-color-text mb-0 topcard__title']"
        company_tag = "//a[@class='topcard__org-name-link topcard__flavor--black-link']"
        button_tag = '//button[text()="\n        Show more\n\n        "]'
        description_tag = "//div[@class='description__text description__text--rich']"
        location_tag = "//span[@class='topcard__flavor topcard__flavor--bullet']"

        driver.get(url)

        # Extract job title, company, and description from the page
        title = get_element(driver, title_tag).text
        company = get_element(driver, company_tag)
        company_name = company.text
        time.sleep(random.uniform(0.0, 0.1))
        get_element(driver, button_tag).click()
        description = get_element(driver, description_tag).text[:-9]  # Remove last 9 characters
        location_element = get_element(driver, location_tag)
        location = location_element.text.strip()
        company_link = company.get_attribute("href")

        logging.debug("Extracted title: %s", title)
        logging.debug("Extracted company: %s", company)
        logging.debug("Extracted description: %s", description)

        return Job(title, company_name, description, url, company_link, location)
    except InvalidURLException:
        # Handle InvalidURLException
        logging.error("Invalid URL format.")
        raise InvalidURLException("Invalid URL format.")
    except (NoSuchElementException, NoSuchAttributeException) as e:
        # Handle PageElementNotFoundError
        logging.error("Unable to find required job elements on the page: %s", e)
        raise PageElementNotFoundError("Unable to find required job elements on the page.")
    except InvalidArgumentException as e:
        # Handle PageLoadError
        logging.error("Failed to load the page: %s", e)
        raise PageLoadError("Failed to load the page.")
    except Exception as e:
        # Handle other ScrapingError
        logging.error("An unexpected error occurred: %s", e)
        raise ScrapingError("An unexpected error occurred.")
    finally:
        driver.quit()

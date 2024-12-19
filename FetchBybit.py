"""
Bybit does not has API to request earn rate. This file use selenium to manually scrape the rate from website page. 
Therefore It won;t work if Bybit change its webpage structure. Also using selenium is slow.
"""
from ExchangeClass import CEX
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class Bybit(CEX):
    def __init__(self, assets = None):
        super().__init__(assets)
        # Configure WebDriver (use Chrome in this example)
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,})# block image loading
        self.chrome_options.add_argument("--headless=new")  # Run in headless mode
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")
        self.service = webdriver.ChromeService()
        self.driver = None
    
    def _StartBrowserDriver(self) -> None:
        if self.driver is None:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        elif self.driver.session_id is None:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        else:
            pass

    def _CloseBrowserDriver(self) -> None:
        self.driver.quit()

    def simpleEarn(self, asset:str) -> dict:
        # Path to the WebDriver (update this path as needed)
        #driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        url = f"https://www.bybit.com/en/earn/savings/?search={asset}&type=4"
        try:
            # Open the webpage
            self.driver.get(url)
            apr_elements = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ant-list-items']")) 
                                                        )
            # Locate all elements with the specified class name
            apr_elements = self.driver.find_element(By.XPATH, '//*[@id="rc-tabs-0-panel-flexible-products"]/div/div[2]/div[1]/div/ul/div/div/div[2]/p')
            webdriver.ActionChains(self.driver).move_to_element_with_offset(apr_elements, 0,-5).pause(1).perform() #mouse over to get hidden tooltip.
            try:
                apr_text = self.driver.find_element(By.CSS_SELECTOR, "[class*='default_container__qrXlR']")
                apr_text = apr_text.text.split("\n")
                rates = []
                for line in apr_text:
                    amt, rate = line.split(":")
                    rate = float(rate.strip().replace('%',''))
                    rates.append({'amt':amt, 'rate':rate})
                return {asset: rates}
            except NoSuchElementException:
                rate = float(apr_elements.text.replace('%',''))
                return {asset: [{'amt':'', 'rate':rate}]}
            except Exception as e:
                print(f"Error extracting APR: {e}")
            return {asset: {'amt':'', 'rate':''}}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {asset: {'amt':'', 'rate':''}}

        finally:
            pass
            # Close the browser
            #driver.quit()
    
    def getSimpleEarnRates(self) -> dict:
        if self.assets is None:
            print(f"{self.assets=}. Add assets first!")
        self._StartBrowserDriver()
        for asset in self.assets:
            self.SimpleEarnRates.update(self.simpleEarn(asset))
        self._CloseBrowserDriver()
        if False:
            if len(self.assets)==1:
                self.SimpleEarnRates.update(self.simpleEarn(self.assets[0]))
            else:
                #Run many selenium instances on multithread.
                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {executor.submit(self.simpleEarn, asset): asset for asset in self.assets}
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            self.SimpleEarnRates.update(result)
                        except Exception as e:
                            print(f"Error processing {futures[future]}: {e}")

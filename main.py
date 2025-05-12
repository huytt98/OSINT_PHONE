from phone_analyzer import analyze_phone_number
from web_searcher import find_related_info, WebSearcher
from social_scanner import SocialScanner
from location_tracker import LocationTracker
from result_formatter import (display_results, display_phone_analysis, 
                            display_progress, display_social_results,
                            display_location_info)
from colorama import init, Fore, Style
from cache_manager import CacheManager
from utils import setup_logging
from tqdm import tqdm
import logging
import asyncio
from data_collector import DataCollector
from datetime import datetime

BANNER = f"""
{Fore.RED}
  ____  _____ _ _   _ _____   ____  _   _  ___  _   _ _____ 
 / __ \/ ____(_) \ | |_   _| |  _ \| | | |/ _ \| \ | | ____|
| |  | | (___ _|  \| | | |   | |_) | |_| | | | |  \| |  _|  
| |  | |\___ \ | . ` | | |   |  _ <|  _  | | | | . ` | |___ 
| |__| |____) | |\  |_| |_  | |_) | | | | |_| | |\  |_____|
 \____/|_____/|_| \_|_____| |____/|_| |_|\___/|_| \_|_____|
{Style.RESET_ALL}
{Fore.CYAN}[*] Phone Number Intelligence Scanner
{Fore.GREEN}[*] Coded By R4v3n
{Fore.YELLOW}[*] Version 1.0
{Style.RESET_ALL}
"""

def get_phone_number():
    """Get phone number from user input."""
    print(f"\n{Fore.CYAN}Enter phone number with country code (e.g., +861xxxxxxxxx): {Style.RESET_ALL}", end="")
    return input()

async def run_analysis(phone, cache_manager):
    logger = logging.getLogger('osint.main')
    collector = DataCollector()
    stages = ['phone', 'location', 'social', 'web']
    
    try:
        async with WebSearcher(cache_manager) as searcher:
            with tqdm(total=len(stages), desc="Analysis Progress") as pbar:
                try:
                    display_progress("Analyzing phone number")
                    analysis = analyze_phone_number(phone)
                    if analysis:
                        display_phone_analysis(analysis)
                        logger.info(f"Phone analysis completed for {phone}")
                    pbar.update(1)
                    
                    display_progress("Tracking location information")
                    tracker = LocationTracker()
                    location_info = tracker.get_location_info(phone)
                    display_location_info(location_info)
                    logger.info(f"Location tracking completed for {phone}")
                    pbar.update(1)
                    
                    display_progress("Scanning social media and email accounts")
                    scanner = SocialScanner()
                    social_results = scanner.find_social_accounts(phone)
                    email_results = scanner.find_email_accounts(phone)
                    display_social_results(social_results, email_results)
                    logger.info(f"Social media and email scanning completed for {phone}")
                    pbar.update(1)
                    
                    display_progress("Searching for related information")
                    search_results = await searcher.search_all_engines(phone)
                    
                    if search_results and isinstance(search_results, dict):
                        analysis = collector.analyze_results(search_results)
                        results_file = collector.save_results(phone, search_results, analysis)
                        display_results(search_results, analysis)
                        logger.info(f"Web search completed for {phone}. Results saved to {results_file}")
                    else:
                        logger.warning("No valid search results found")
                        display_results({'search_results': [], 'search_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    
                    pbar.update(1)
                except Exception as e:
                    logger.error(f"Error during analysis: {e}")
                    raise
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise
    finally:
        # Cleanup code here if needed
        pass

def main():
    print(BANNER)
    logger = setup_logging()
    init()  # Initialize colorama
    cache_manager = CacheManager()
    
    phone = get_phone_number()
    if phone:
        try:
            asyncio.run(run_analysis(phone, cache_manager))
            logger.info("Analysis completed successfully")
            print(f"\n{Fore.GREEN}Analysis completed!{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            print(f"\n{Fore.RED}Error during analysis: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

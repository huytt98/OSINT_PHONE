from colorama import init, Fore, Back, Style
from datetime import datetime

# Initialize colorama
init()

def _print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}" + "="*50)
    print(f" {text} ".center(50, "="))
    print("="*50 + f"{Style.RESET_ALL}")

def _print_section(text):
    """Print a formatted section header."""
    print(f"\n{Fore.GREEN}{Style.BRIGHT}{text}")
    print("-" * len(text) + f"{Style.RESET_ALL}")

def display_results(results, analysis=None):
    """Display search results in a formatted way."""
    _print_header("Search Results Summary")
    
    if not results:
        print(f"\n{Fore.YELLOW}No significant information found.{Style.RESET_ALL}")
        return
    
    if 'search_time' in results:
        print(f"{Fore.YELLOW}Search Time: {results['search_time']}{Style.RESET_ALL}\n")
    
    if analysis:
        _print_section("📊 Result Analysis")
        print(f"{Fore.WHITE}Total Results: {Fore.CYAN}{analysis['total_results']}{Style.RESET_ALL}")
        
        # Display categories
        _print_section("🏷️ Categories")
        for category, urls in analysis['categories'].items():
            if urls:
                print(f"\n{Fore.GREEN}{category.replace('_', ' ').title()}: {Style.RESET_ALL}")
                for idx, url in enumerate(urls, 1):
                    print(f"{Fore.CYAN}{idx:02d}.{Style.RESET_ALL} {url}")
        
        # Display top domains
        _print_section("🔝 Top Domains")
        sorted_domains = sorted(analysis['domain_frequency'].items(), 
                              key=lambda x: x[1], reverse=True)[:5]
        for domain, count in sorted_domains:
            print(f"{Fore.WHITE}{domain}: {Fore.CYAN}{count} results{Style.RESET_ALL}")
    
    if 'search_results' in results:
        _print_section("🔍 Search Results")
        for idx, url in enumerate(results['search_results'], 1):
            print(f"{Fore.CYAN}{idx:02d}.{Style.RESET_ALL} {url}")
    
    # Show search statistics
    total_results = len(results.get('search_results', []))
    print(f"\n{Fore.GREEN}Total Results Found: {total_results}{Style.RESET_ALL}")

def display_phone_analysis(analysis):
    """Display phone number analysis in a formatted way."""
    if not analysis:
        return
    
    _print_header("Phone Number Analysis")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.YELLOW}Analysis Time: {current_time}{Style.RESET_ALL}")
    
    # Basic information
    _print_section("📱 Basic Information")
    print(f"{Fore.WHITE}Formatted Number: {Fore.CYAN}{analysis['formatted']['international']}")
    print(f"{Fore.WHITE}Country: {Fore.CYAN}{analysis['country']}")
    print(f"{Fore.WHITE}Carrier: {Fore.CYAN}{analysis['carrier'] or 'Unknown'}")
    
    # Technical details
    _print_section("🔧 Technical Details")
    print(f"{Fore.WHITE}Number Type: {Fore.CYAN}{analysis['number_type']}")
    print(f"{Fore.WHITE}Country Code: {Fore.CYAN}+{analysis['country_code']}")
    print(f"{Fore.WHITE}National Number: {Fore.CYAN}{analysis['national_number']}")
    
    # Additional information
    _print_section("ℹ️ Additional Information")
    print(f"{Fore.WHITE}Time Zones: {Fore.CYAN}{', '.join(analysis['timezones'])}")
    
    # Validation status
    _print_section("✓ Validation Status")
    valid_color = Fore.GREEN if analysis['is_valid'] else Fore.RED
    possible_color = Fore.GREEN if analysis['possibility'] else Fore.RED
    print(f"Valid Number: {valid_color}{'✓' if analysis['is_valid'] else '✗'}{Style.RESET_ALL}")
    print(f"Possible Number: {possible_color}{'✓' if analysis['possibility'] else '✗'}{Style.RESET_ALL}")

def display_progress(message):
    """Display a progress message."""
    print(f"\n{Fore.BLUE}⏳ {message}...{Style.RESET_ALL}")

def display_social_results(social_results, email_results):
    """Display social media and email results."""
    _print_header("Social Media & Email Analysis")
    
    # Display social media results
    _print_section("🌐 Social Media Accounts")
    if social_results:
        for platform, url in social_results.items():
            print(f"{Fore.WHITE}{platform.title()}: {Fore.CYAN}{url}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No social media accounts found.{Style.RESET_ALL}")
    
    # Display possible email accounts
    _print_section("📧 Possible Email Accounts")
    if email_results:
        for idx, email in enumerate(email_results, 1):
            print(f"{Fore.WHITE}{idx}. {Fore.CYAN}{email}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No potential email accounts found.{Style.RESET_ALL}")

def display_location_info(location_info):
    """Display location information."""
    if not location_info:
        return
        
    _print_header("📍 Location Information")
    
    print(f"{Fore.WHITE}Country: {Fore.CYAN}{location_info['country']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Carrier Region: {Fore.CYAN}{location_info['carrier']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Detailed Location: {Fore.CYAN}{location_info['city']}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}GPS Coordinates:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Latitude: {location_info['latitude']}")
    print(f"Longitude: {location_info['longitude']}{Style.RESET_ALL}")
    
    if location_info['map_file']:
        print(f"\n{Fore.GREEN}Map generated: {location_info['map_file']}{Style.RESET_ALL}")
    
    if location_info['approximate']:
        print(f"\n{Fore.YELLOW}Note: Location is approximate based on carrier and country data{Style.RESET_ALL}")

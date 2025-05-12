import json
import os
from datetime import datetime
from urllib.parse import urlparse
from collections import defaultdict

class DataCollector:
    def __init__(self, output_dir="results"):
        self.output_dir = os.path.join(os.path.dirname(__file__), output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_results(self, results):
        """Analyze and categorize search results."""
        categories = defaultdict(list)
        domains = defaultdict(int)
        
        for url in results.get('search_results', []):
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Categorize URL
            if any(x in domain for x in ['linkedin', 'facebook', 'twitter']):
                categories['social_media'].append(url)
            elif '.gov' in domain:
                categories['government'].append(url)
            elif any(x in url for x in ['.pdf', '.doc', '.txt']):
                categories['documents'].append(url)
            elif any(x in url for x in ['contact', 'about', 'profile']):
                categories['contact_info'].append(url)
            else:
                categories['others'].append(url)
            
            domains[domain] += 1
        
        return {
            'categories': dict(categories),
            'domain_frequency': dict(domains),
            'total_results': len(results.get('search_results', [])),
            'timestamp': datetime.now().isoformat()
        }

    def save_results(self, phone_number, results, analysis):
        """Save results and analysis to file."""
        filename = f"results_{phone_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        data = {
            'phone_number': phone_number,
            'search_results': results,
            'analysis': analysis,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'result_count': len(results.get('search_results', []))
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath

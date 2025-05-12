# Phone Number OSINT Tool

<p align="center">
  <img src="banner.png" alt="R4v3n OSINT Tool"/>
</p>

> Developed by R4v3n  
> Version 1.0

An advanced OSINT (Open Source Intelligence) tool for phone number analysis and information gathering.

## Features

- 📱 Detailed Phone Analysis
  - Country and region detection
  - Carrier identification
  - Number type classification
  - Validation and formatting
  - Timezone detection

- 🌍 Location Intelligence
  - Approximate geolocation
  - Interactive map visualization
  - Carrier region mapping
  - GPS coordinates
  - Location caching

- 🔍 Multi-Platform Search
  - Google, Bing, Yandex integration
  - Advanced search operators
  - Batch processing
  - Rate-limited requests
  - Proxy rotation

- 👥 Social Media Scanner
  - Popular platforms coverage
  - Account discovery
  - Profile linking
  - Automated verification

- 📧 Email Discovery
  - Pattern-based search
  - Common email services
  - Association analysis
  - Validation checks

- 💾 Performance Features
  - Smart caching system
  - Memory management
  - Connection pooling
  - Async operations
  - Rate limiting

## Installation

```bash
# Clone the repository
git clone [repository-url]

# Navigate to project directory
cd OSINT-PHONE-NUMBER

# Install required packages
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Enter phone number in international format (e.g., +1234567890)

## Project Structure

```
OSINT-PHONE-NUMBER/
├── main.py              # Entry point and orchestration
├── phone_analyzer.py    # Phone number analysis
├── web_searcher.py      # Web search operations
├── social_scanner.py    # Social media scanning
├── location_tracker.py  # Location services
├── data_collector.py    # Data aggregation
├── result_formatter.py  # Output formatting
├── cache_manager.py     # Cache operations
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## Output Directories

- `/results` - Search results and analysis
- `/maps` - Generated location maps
- `/logs` - Operation logs
- `/cache` - Cached data

## Features in Detail

### Phone Analysis
- Country code detection
- Carrier identification
- Number type classification
- Format validation
- Regional analysis

### Location Tracking
- Carrier-based geolocation
- Interactive map generation
- Area visualization
- Coordinate mapping

### Web Search
- Multi-engine integration
- Advanced search operators
- Result categorization
- Domain analysis
- Content classification

### Social Media
- Platform detection
- Account verification
- Profile discovery
- Automated scanning

## Technical Features

- Asynchronous operations
- Connection pooling
- Rate limiting
- Proxy rotation
- Memory management
- Error handling
- Result caching
- Logging system

## Requirements

- Python 3.7+
- Internet connection
- Required packages in requirements.txt

## Notes

- Uses only publicly available data
- Respects rate limits and terms of service
- Results may vary based on available data
- Some features require API keys

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Author

**R4v3n**
- GitHub: [@R4v3n](https://github.com/R4v3n)

## License

Copyright © 2024 R4v3n  
This project is MIT licensed.


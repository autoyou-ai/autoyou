# AutoYou - Robinhood Chat Trading Agent

**AutoYou** is an intelligent trading assistant that enables users to interact with their Robinhood accounts through natural language conversations. Built on Google's Agent Development Kit (ADK), AutoYou provides a secure, AI-powered interface for portfolio management, stock analysis, options trading, and order execution - all through simple chat commands.

> **⚠️ IMPORTANT DISCLAIMER**: AutoYou is an experimental tool for educational and personal use only. It is NOT financial advice. All trading decisions are your responsibility. See full disclaimer below.

## 🚀 Key Features

### **Comprehensive Trading Operations**
- **Portfolio Management**: Real-time portfolio overview, holdings analysis, and performance tracking
- **Stock Research**: Live stock prices, financial metrics, news, earnings, and historical data
- **Options Trading**: Options discovery, Greeks analysis, position tracking, and complex strategies
- **Order Management**: Place, modify, and cancel orders for stocks, options, and cryptocurrencies
- **Market Intelligence**: Market trends, top movers, S&P 500 analysis, and sector performance

### **Intelligent Agent Architecture**
- **Specialized Sub-Agents**: Dedicated agents for login, portfolio, stocks, options, orders, and markets
- **Safety-First Trading**: Mandatory confirmation workflows for all trading operations
- **Loop Prevention**: Advanced detection and prevention of infinite agent transfer cycles
- **Session Analytics**: Comprehensive tracking and analysis of user interactions

### **Cross-Platform Deployment**
- **Mobile Apps**: Native iOS and Android apps using Kivy framework
- **Web Interface**: FastAPI-powered web application with ADK integration
- **Desktop Support**: Windows, macOS, and Linux desktop applications
- **Secure Storage**: Cross-platform credential management with JsonStore

### **Security & Privacy**
- **Local Processing**: All financial data processed locally - no sensitive data sent to external LLMs
- **Encrypted Storage**: Secure credential storage using platform-native encryption
- **Session Management**: TinyDB-powered session tracking with analytics
- **API Security**: Direct integration with Robinhood APIs without third-party intermediaries

## 💬 Use Cases & Examples

### **Portfolio Management**
```
"Show me my portfolio overview"
"What's my current buying power?"
"How did my investments perform this week?"
"Add AAPL to my watchlist"
"Show me my dividend history"
```

### **Stock Research & Analysis**
```
"What's the current price of Tesla?"
"Show me Apple's financial metrics"
"Get me the latest news on NVDA"
"What are the top moving stocks today?"
"Show me MSFT's earnings history"
```

### **Options Trading**
```
"Find call options for AAPL expiring next Friday"
"Show me my current options positions"
"What are the Greeks for my SPY puts?"
"Find profitable put options for QQQ"
"Show me the option chain for TSLA"
```

### **Order Management**
```
"Buy 10 shares of Apple at market price"
"Place a limit order to sell 50 shares of TSLA at $250"
"Cancel my open order for NVDA"
"Show me my order history for this week"
"Buy $500 worth of Bitcoin"
```

### **Market Intelligence**
```
"What are today's top market movers?"
"How is the S&P 500 performing?"
"Show me market trends for tech stocks"
"What sectors are performing best today?"
```

## 🛡️ Security & Safety Features

### **Financial Data Protection**
- **Zero LLM Exposure**: No sensitive financial data is ever sent to external language models
- **Local Processing**: All trading decisions and analysis happen locally on your device
- **Encrypted Storage**: Credentials stored using platform-native encryption (Keychain on iOS, etc.)
- **Session Isolation**: Each trading session is isolated with comprehensive analytics

### **Trading Safety Protocols**
- **Mandatory Confirmation**: All trading operations require explicit user confirmation
- **Order Validation**: Comprehensive validation of order parameters before execution
- **Loop Prevention**: Advanced detection prevents infinite agent transfer cycles
- **Error Handling**: Graceful error handling with clear user feedback
- **Immediate Abort**: Any uncertainty or user hesitation immediately cancels operations

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+ installed
- Robinhood account with API access
- Google API key for ADK integration

### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/autoyou.git
cd autoyou

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### **Running the Application**

#### **Web Interface**
```bash
# Start the web server
python main.py

# Open browser to http://127.0.0.1:8000/dev-ui/?app=autoyou
```

#### **Desktop Application**
```bash
# Run as desktop app
python main.py --desktop
```

## 📱 Multi-Platform Deployment

### **iOS Deployment**

#### **Requirements**
- macOS with Xcode 15.2+
- iOS Developer Account
- kivy-ios toolchain

#### **Build Process**
```bash
# Install kivy-ios
pip install kivy-ios

# Create iOS project
toolchain build python3 kivy
toolchain create AutoYou .

# Build for device
cd AutoYou-ios
xcodebuild -project AutoYou.xcodeproj -scheme AutoYou -configuration Release
```

#### **Deployment Steps**
1. Open `AutoYou.xcodeproj` in Xcode
2. Configure signing & capabilities
3. Set deployment target (iOS 12.0+)
4. Build and archive for App Store or TestFlight

### **Android Deployment**

#### **Requirements**
- Android SDK and NDK
- Java Development Kit (JDK) 8+
- Buildozer for packaging

#### **Build Process**
```bash
# Install buildozer
pip install buildozer

# Initialize buildozer
buildozer init

# Build APK
buildozer android debug

# Build for release
buildozer android release
```

#### **Configuration**
Edit `buildozer.spec`:
```ini
[app]
title = AutoYou
package.name = autoyou
package.domain = com.yourcompany.autoyou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,kivymd,requests,robin-stocks

[buildozer]
log_level = 2
```

### **Windows Desktop**

#### **Using PyInstaller**
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed main.py

# Create installer with NSIS
makensis autoyou-installer.nsi
```

#### **Using cx_Freeze**
```bash
# Install cx_Freeze
pip install cx_Freeze

# Build executable
python setup.py build
```

### **macOS Desktop**

#### **Using PyInstaller**
```bash
# Create macOS app bundle
pyinstaller --onefile --windowed --osx-bundle-identifier com.yourcompany.autoyou main.py

# Create DMG installer
hdiutil create -volname "AutoYou" -srcfolder dist/AutoYou.app -ov -format UDZO AutoYou.dmg
```

### **Linux Desktop**

#### **AppImage Creation**
```bash
# Install python-appimage
pip install python-appimage

# Create AppImage
python-appimage build app main.py
```

#### **Snap Package**
```bash
# Create snapcraft.yaml
snapcraft init

# Build snap
snapcraft

# Install locally
sudo snap install autoyou_1.0_amd64.snap --dangerous
```

## 🔧 Development Setup

### **Environment Configuration**
Create `.env` file:
```env
# Robinhood Credentials
ROBINHOOD_USERNAME=your_username
ROBINHOOD_PASSWORD=your_password
ROBINHOOD_MFA_CODE=your_mfa_code  # Optional

# Google API
GOOGLE_API_KEY=your_google_api_key

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

### **Testing**
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/

# Test agent functionality
python test_agent_with_sessions.py
```

### **Development Dependencies**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install
```

## 🏗️ Architecture Overview

### **System Components**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface │    │   Agent Layer    │    │  External APIs  │
│                 │    │                  │    │                 │
│ • Kivy Mobile   │◄──►│ • AutoYou Agent  │◄──►│ • Robinhood API │
│ • Web Interface │    │ • Sub-Agents     │    │ • Google ADK    │
│ • Desktop App   │    │ • Session Mgmt   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Local Storage   │    │   Security Layer │    │   Analytics     │
│                 │    │                  │    │                 │
│ • JsonStore     │    │ • Encryption     │    │ • TinyDB        │
│ • TinyDB        │    │ • Validation     │    │ • Session Data  │
│ • Credentials   │    │ • Confirmation   │    │ • Performance   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Agent Hierarchy**
- **AutoYou Root Agent**: Main coordinator with loop prevention and safety protocols
- **Robinhood Login Agent**: Secure authentication and session management
- **Portfolio Agent**: Account overview, holdings, performance tracking
- **Stocks Agent**: Research, pricing, news, fundamentals, earnings
- **Options Agent**: Discovery, Greeks analysis, position tracking
- **Orders Agent**: Trading operations with mandatory confirmation workflows
- **Markets Agent**: Market trends, top movers, sector analysis

## 📁 Project Structure

```
autoyou/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
├── README.md                  # This file
│
├── autoyou_agent/             # Core agent implementation
│   ├── agent.py              # Main AutoYou agent
│   ├── prompt.py             # Agent instructions and prompts
│   └── sub_agents/           # Specialized trading agents
│       ├── robinhood_login/
│       ├── robinhood_portfolio/
│       ├── robinhood_stocks/
│       ├── robinhood_options/
│       ├── robinhood_orders/
│       └── robinhood_markets/
│
├── tests/                     # Test suite
│   ├── test_agent_with_sessions.py
│   ├── comprehensive_test.py
│   └── test_session_integration.py
│
└── docs/                      # Documentation
    ├── deployment.md
    ├── api_reference.md
    └── troubleshooting.md
```

## 🔧 Advanced Configuration

### **Environment Variables**
```env
# Core Configuration
DEBUG=false
LOG_LEVEL=INFO
PORT=8000
HOST=127.0.0.1

# Robinhood Configuration
ROBINHOOD_USERNAME=your_username
ROBINHOOD_PASSWORD=your_password
ROBINHOOD_MFA_CODE=123456  # Optional, for 2FA
ROBINHOOD_DEVICE_TOKEN=your_device_token  # Optional

# Google ADK Configuration
GOOGLE_API_KEY=your_google_api_key
GOOGLE_PROJECT_ID=your_project_id

# Security Settings
SESSION_TIMEOUT=3600  # Session timeout in seconds
MAX_LOGIN_ATTEMPTS=3
ENCRYPTION_KEY=your_encryption_key

# Trading Safety
MAX_ORDER_VALUE=10000  # Maximum single order value
REQUIRE_CONFIRMATION=true
ENABLE_PAPER_TRADING=false

# Analytics
ENABLE_ANALYTICS=true
ANALYTICS_RETENTION_DAYS=30
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Installation Problems**
```bash
# Kivy installation issues on macOS
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer

# Android build issues
export ANDROID_HOME=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# iOS build issues (macOS only)
xcode-select --install
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

#### **Runtime Errors**
```bash
# Check logs
tail -f ~/.autoyou/logs/autoyou.log

# Verify dependencies
python -c "import kivy, robin_stocks, google.adk; print('All imports successful')"

# Test Robinhood connection
python -c "import robin_stocks as r; print(r.robinhood.authentication.login('user', 'pass'))"
```

#### **Agent Issues**
- **Loop Detection Triggered**: Check query complexity, try more specific requests
- **Login Failures**: Verify credentials, check 2FA settings, ensure account access
- **Order Failures**: Check buying power, market hours, order parameters
- **Data Issues**: Verify API keys, check network connectivity, review rate limits

### **Debug Mode**
```bash
# Enable comprehensive debugging
DEBUG=true LOG_LEVEL=DEBUG python main.py

# Test specific components
python -m autoyou_agent.tests.test_agent_with_sessions
python comprehensive_test.py
```

## 🤝 Contributing

### **Development Workflow**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with tests
4. Run test suite: `python -m pytest`
5. Submit pull request

### **Code Standards**
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation as needed

### **Testing Requirements**
```bash
# Run full test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest --cov=autoyou_agent tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

## 📄 Legal & Compliance

### **Important Disclaimers**

**⚠️ EXPERIMENTAL SOFTWARE NOTICE**
AutoYou is experimental software intended for educational and personal use only. It is NOT:
- Financial advice or investment recommendations
- A licensed financial advisory service
- Guaranteed to be error-free or profitable
- Suitable for production trading without thorough testing

**📋 USER RESPONSIBILITIES**
By using AutoYou, you explicitly acknowledge and agree that:
- You assume full responsibility for all trading decisions
- You understand financial markets are inherently risky
- You will conduct independent research before trading
- You will only trade with money you can afford to lose
- You will comply with all applicable laws and regulations

**🛡️ LIABILITY LIMITATIONS**
The developers, contributors, and affiliated parties disclaim all liability for:
- Financial losses or opportunity costs
- Software bugs, errors, or malfunctions
- Data loss or security breaches
- Regulatory compliance issues
- Any direct, indirect, or consequential damages

### **Privacy Policy**
- **Data Collection**: Only essential data for functionality is collected
- **Data Storage**: All sensitive data stored locally on your device
- **Data Sharing**: No personal or financial data shared with third parties
- **Analytics**: Optional usage analytics for improvement (can be disabled)

### **Terms of Service**
- Software provided "as-is" without warranties
- Users must comply with Robinhood's Terms of Service
- Users must comply with applicable securities regulations
- Modification and redistribution permitted under MIT License

## 📞 Support & Community

### **Getting Help**
1. **Documentation**: Check this README and `/docs` folder
2. **Issues**: Search [GitHub Issues](https://github.com/yourusername/autoyou/issues)
3. **Discussions**: Join [GitHub Discussions](https://github.com/yourusername/autoyou/discussions)
4. **Community**: Follow development updates and announcements

### **Reporting Issues**
When reporting issues, please include:
- Operating system and version
- Python version and environment details
- Complete error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior

### **Feature Requests**
We welcome feature requests! Please:
- Check existing issues and discussions first
- Provide detailed use case descriptions
- Consider contributing the implementation
- Follow the issue template guidelines

## 🙏 Acknowledgments

- **Google ADK Team**: For the powerful Agent Development Kit framework
- **Kivy Community**: For the excellent cross-platform mobile framework
- **Robinhood**: For providing accessible trading APIs
- **Open Source Contributors**: For the amazing libraries and tools
- **Trading Community**: For feedback, testing, and feature suggestions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the trading community**

*AutoYou - Your Personal Trading Assistant*

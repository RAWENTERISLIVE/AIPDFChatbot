# Security Policy

## 🔒 Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | ✅ Yes            |
| 1.x.x   | ❌ No             |

## 🛡️ Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 🚨 For Critical Security Issues
- **DO NOT** open a public GitHub issue
- Email us directly at: [Your Security Email]
- Include detailed information about the vulnerability
- We'll respond within 24-48 hours

### 📋 What to Include
- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Any suggested fixes (if you have them)

## 🔐 Security Best Practices

### For Users
- **Never commit your `.env` file** with API keys to version control
- **Rotate your API keys** regularly
- **Run the application** in a secure environment
- **Monitor logs** for suspicious activity

### For Developers
- **Validate all inputs** thoroughly
- **Use environment variables** for sensitive data
- **Follow secure coding practices**
- **Test security features** before releasing

## 🛠️ Security Features

### Current Protections
- ✅ **API Key Protection**: Environment variables only
- ✅ **Input Validation**: File type and size validation
- ✅ **Rate Limiting**: Built-in API rate limit handling
- ✅ **Process Isolation**: Separate server/client processes
- ✅ **Clean Shutdown**: Proper resource cleanup

### Planned Enhancements
- 🔄 **Authentication System**: User login and session management
- 🔄 **Access Controls**: Role-based permissions
- 🔄 **Audit Logging**: Security event logging
- 🔄 **HTTPS Support**: Encrypted communication

## ⚠️ Known Considerations

### Current Limitations
- Application runs on localhost by default
- No built-in user authentication
- API keys stored in plain text (environment variables)

### Recommendations
- Use in trusted environments
- Consider network restrictions if exposing externally
- Implement additional authentication for production use

## 📞 Contact

For security-related questions or concerns:
- Open a general issue on GitHub (for non-sensitive topics)
- Email: [Your Security Email] (for sensitive security matters)

## 🙏 Acknowledgments

We appreciate the security research community and will acknowledge responsible disclosure contributors (with permission).

**Thank you for helping keep AI PDF Chatbot secure!** 🔒

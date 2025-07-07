# Democratize AI Toolkit

> Minimal AI access and information sovereignty for everyone

## Demo
### Demo of Ollama and Gemma 3 1B on an Ubuntu Terminal
https://www.youtube.com/watch?v=joCcloRsYl8

### Demo of SSH Access to Ubuntu Running Gemma3 1B
https://youtube.com/shorts/qoASaeTOZVg

## Philosophy

**Equal access to AI should not depend on economic circumstances.**

This toolkit provides two fundamental solutions:
- **Local AI Chat**: Direct access to Gemma 3 1B without cloud dependencies
- **Information Umbrella**: Static defense against information overload and fake news

## Why Gemma 3 1B + Minimal Structure

**Data Sovereignty**: Your conversations stay on your hardware. No surveillance, no data mining, no external dependencies.

**Economic Accessibility**: A 70,000 yen mini PC can serve an entire classroom in developing regions through SSH access.

**Educational Focus**: Minimal starter code teaches principles, not just tools. Students build their own features.

**Resilience**: Static files and local AI survive internet censorship, infrastructure failures, and algorithmic manipulation.

## Components

### 1. CLI Chat (`cli-chat/`)
Local AI conversation with history search and educational expansion framework.

**Requirements:**
```bash
pip install ollama rich
```

**Quick Start:**
```bash
ollama serve
ollama pull gemma3:1b
python gemma_chat_en.py
```

### 2. Information Umbrella (`info-umbrella/`)
Curated global news sources in a single HTML file. Zero JavaScript, zero tracking, infinite scalability.

**Usage:** Set `info-umbrella-2001-08-01.html` as your browser homepage.

https://trgr-karasutoragara.github.io/zen-info-your-life-is-yours/info-umbrella-2001-08-01.html

## Multi-User Access

**Experiment with SSH access** from smartphones, Chromebooks, and PCs. Test your system's limits and learn resource management through hands-on experience.

## Defense Against Information Warfare

**Problem**: Fake news scales exponentially. Traditional fact-checking cannot keep pace.

**Solution**: Static whitelists scale infinitely at near-zero cost. When fake news multiplies by 100 million, curated HTML files become relatively stronger.

**Cost Advantage**: Defense through simplicity rather than expensive algorithmic arms races.

## Global Impact

This toolkit addresses:
- **Digital Divide**: Local AI eliminates cloud subscription barriers
- **Information Asymmetry**: Curated sources level the playing field
- **Educational Inequality**: Self-extension framework teaches real skills
- **Technological Sovereignty**: No dependence on foreign cloud services

## /.md: Reading focused markdown viewer with note-taking.
A new addition to this series is now available. Learn more here → [link](https://github.com/trgr-karasutoragara/zen-info-your-life-is-yours/)

## License

MIT License - Use freely, modify freely, distribute freely.

## Final Message

**Use this for your happiness.**

Technology should serve human flourishing, not corporate profits. This toolkit belongs to you.

---

*"百戰百勝、非善之善者也" - Victory without wisdom is not true skill. — Sun Tzu*

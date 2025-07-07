# /.md
Reading focused markdown viewer with note-taking.

## Demo
https://youtu.be/llXxeGwUa0k?si=v77H3hg38fGreRC8

## Screenshots

| **Home screen** | **Screen with a Markdown (.md) file open** |
| :---: | :---: |
| <img src="https://github.com/trgr-karasutoragara/zen-info-your-life-is-yours/blob/main/md/img/Screenshot-2025-07-07-17-54-49.png" width="400"> | <img src="https://github.com/trgr-karasutoragara/zen-info-your-life-is-yours/blob/main/md/img/Screenshot-2025-07-07-17-24-36.png" width="400"> |

## Purpose
Read markdown files while taking notes. Export notes when finished.


## File Loading
Click "Open Files" button to select .md files
Use "open" command
Drag and drop .md files anywhere


## Commands
open - Select local files
load - Load file from list
add - Add reading note
record list - Show all notes
export - Export notes to file


## Simple Workflow
Open your .md files (button or drag/drop)
Read and take notes with "add"
Export notes when done
Focus on reading and note-taking


## Background of Development
Infrastructure varies greatly across countries and regions. In some cases, communication costs can consume around 10% of a person's income. Tools that continue to function even when infrastructure is damaged—such as during disasters—can be especially valuable.

## This Tool is a Prototype
It functions properly on the iPhone SE (3rd generation), but we have confirmed that opening a .md file on the Google Pixel 7a can cause the screen to freeze. It works on Chromebooks.
If you like it, please feel free to extend it to suit your needs.

## What This Tool Offers
Clarification of the Problem: This tool addresses a specific issue—“I want to read a large number of Markdown files while taking fragmented notes as I think.”
     ↓
Prototype Solution: This HTML file is a working prototype of that solution.

## The Value of This Tool
**Beauty**: Functional elegance and code simplicity.
**Strength**: Minimal dependencies and a clear guiding philosophy.
**Kindness**: Open and accessible—anyone can use and modify it.

## Why Is There No Text Editor?

To keep things simple

To help you stay focused while reading

Because notes recorded via the add command can be exported and formatted later

## The Implemented Philosophy
Single HTML File: No installation required—just open it in your browser. Maximum portability and accessibility.
Offline-First: External libraries are loaded via CDN, but once cached, the tool works fully offline. All data is stored within the browser.
Terminal-Style UI: The concept of a “Linux terminal-like dark mode” is implemented not only visually but also through command-based interaction. A minimalist design that eliminates distractions and enhances focus.
Mobile-Friendly: Uses a detectDevice() function to identify mobile devices and adjust layout accordingly. Reflects the philosophy of usability in any environment.
Minimalism: The decision not to include a built-in editor is intentional. This tool focuses on “reading and recording thoughts in the moment”—a clear and deliberate philosophy. It resists feature bloat and concentrates on core value.

## Precise Technical Choices
Vanilla JavaScript: Written without any frameworks, using pure JavaScript. This ensures a lightweight tool with minimal dependencies—a design aimed at “no maintenance needed.”
marked.js: Uses the de facto standard for Markdown rendering via CDN. A smart choice that avoids reinventing the wheel and makes use of a reliable external resource.
Command-Line Interface (CLI): Offers both GUI buttons and CLI commands, making it accessible to both beginners and power users. Commands like load, add, and export are intuitive and elegant.
Data Structure: A simple in-memory database object separates files, reading notes (records), and reading positions (positions). This design is clever and extensible, with future scalability in mind (such as potential SQL integration).

---
## .PDF to .md - Minimal PDF to Markdown Converter

Educational starter kit for document processing and accessibility

https://github.com/trgr-karasutoragara/zen-info-your-life-is-yours/blob/main/md/pdf_to_md.py

---

MIT licensed HTML file - you're free to add or remove features as needed. SQL persistence, advanced queries, or any extensions you desire.

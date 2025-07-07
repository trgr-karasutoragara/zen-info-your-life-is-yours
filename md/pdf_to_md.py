#!/usr/bin/env python3
"""
.PDF to .md - Minimal PDF to Markdown Converter
Educational starter kit for document processing and accessibility

Required packages:
pip install pymupdf

OCR Extension Hints:
# Add 'pip install pdf2image pytesseract pillow' and system tesseract for scanned PDFs
# Use pytesseract.image_to_data() with confidence thresholds to filter low-quality text
# Convert PDF pages to images first with convert_from_path() before OCR processing

Educational Philosophy:
- Start with simple text extraction, build understanding before complexity
- Extend yourself: add OCR, web interface, batch processing, authentication
- Resource-conscious design for developing regions and educational institutions
- Learn by building: this is a foundation, not a complete solution

Usage:
python pdf_to_md.py document.pdf
python pdf_to_md.py document.pdf output.md
python pdf_to_md.py document.pdf --verbose

"""

import fitz  # PyMuPDF - lightweight and reliable PDF processing
import re
import sys
import os
import argparse
from pathlib import Path

class PDFToMarkdownConverter:
    """
    Minimal PDF to Markdown converter focusing on educational value and extensibility.
    
    This class demonstrates fundamental document processing concepts:
    - Text extraction from digital PDFs
    - Font analysis for document structure detection  
    - Hierarchical content organization
    - Markdown generation with proper formatting
    
    Designed as a learning foundation that students can extend with:
    - OCR capabilities for scanned documents
    - Web interfaces (Flask/FastAPI)
    - Batch processing systems
    - Multi-language support
    - Advanced layout analysis
    """
    
    def __init__(self, verbose=False):
        """
        Initialize converter with configurable settings.
        
        The verbose flag demonstrates how to build user-friendly tools
        that provide appropriate feedback during long-running operations.
        """
        self.verbose = verbose
        
        # These thresholds can be adjusted based on document types
        # Students should experiment with different values for their use cases
        self.heading_font_threshold = 14.0  # Fonts larger than this become headings
        self.line_spacing_threshold = 1.5    # Line spacing for paragraph breaks
        
        # Statistics tracking for educational feedback
        self.stats = {
            'pages_processed': 0,
            'text_blocks_found': 0,
            'headings_detected': 0,
            'paragraphs_created': 0,
            'list_items_found': 0
        }
    
    def log(self, message):
        """
        Simple logging system that demonstrates good software practices.
        
        In larger applications, this would integrate with Python's logging module.
        This pattern teaches students about user feedback and debugging.
        """
        if self.verbose:
            print(f"[.PDF to .md] {message}")
    
    def analyze_pdf_structure(self, pdf_path):
        """
        Analyze PDF to understand its structure and content type.
        
        This analysis helps determine the best processing strategy
        and provides educational insights about document characteristics.
        Returns a dictionary with analysis results.
        """
        try:
            doc = fitz.open(pdf_path)
            analysis = {
                'total_pages': len(doc),
                'has_text_content': False,
                'avg_chars_per_page': 0,
                'font_sizes_found': set(),
                'estimated_type': 'unknown'
            }
            
            total_chars = 0
            sample_pages = min(3, len(doc))  # Sample first 3 pages for analysis
            
            self.log(f"Analyzing {sample_pages} sample pages from {len(doc)} total pages")
            
            for page_num in range(sample_pages):
                page = doc[page_num]
                
                # Extract text with formatting information
                blocks = page.get_text("dict")
                page_chars = 0
                
                for block in blocks.get("blocks", []):
                    if block.get("type") == 0:  # Text blocks only
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                if text:
                                    page_chars += len(text)
                                    font_size = span.get("size", 0)
                                    analysis['font_sizes_found'].add(round(font_size, 1))
                
                total_chars += page_chars
            
            # Calculate metrics for document type detection
            analysis['avg_chars_per_page'] = total_chars / sample_pages if sample_pages > 0 else 0
            analysis['has_text_content'] = analysis['avg_chars_per_page'] > 50
            
            # Determine document type based on content analysis
            if analysis['avg_chars_per_page'] > 200:
                analysis['estimated_type'] = 'text_rich'
            elif analysis['avg_chars_per_page'] > 50:
                analysis['estimated_type'] = 'text_sparse'
            else:
                analysis['estimated_type'] = 'image_based'
            
            doc.close()
            
            self.log(f"Analysis complete: {analysis['estimated_type']} document with {analysis['avg_chars_per_page']:.1f} chars/page")
            
            return analysis
            
        except Exception as e:
            self.log(f"Analysis failed: {e}")
            return {'estimated_type': 'error', 'error': str(e)}
    
    def extract_structured_content(self, pdf_path):
        """
        Extract text content with structural information preserved.
        
        This method demonstrates how to process PDF text blocks while maintaining
        information about fonts, positions, and formatting that helps determine
        document structure (headings, paragraphs, lists).
        
        Returns a list of content elements with type and formatting metadata.
        """
        try:
            doc = fitz.open(pdf_path)
            content_elements = []
            
            self.log(f"Processing {len(doc)} pages for content extraction")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                self.stats['pages_processed'] += 1
                
                # Get text blocks with detailed formatting information
                blocks = page.get_text("dict")
                
                for block in blocks.get("blocks", []):
                    if block.get("type") == 0:  # Process text blocks only
                        self.stats['text_blocks_found'] += 1
                        block_elements = self._process_text_block(block, page_num + 1)
                        content_elements.extend(block_elements)
            
            doc.close()
            
            self.log(f"Extraction complete: {len(content_elements)} content elements found")
            
            return content_elements
            
        except Exception as e:
            self.log(f"Content extraction failed: {e}")
            return []
    
    def _process_text_block(self, block, page_number):
        """
        Process individual text blocks to extract lines with formatting information.
        
        This internal method shows how to handle the detailed structure that
        PyMuPDF provides, converting it into a more manageable format for
        document structure analysis.
        """
        elements = []
        
        for line in block.get("lines", []):
            line_text = ""
            font_sizes = []
            font_flags = []
            
            # Combine all spans in a line while tracking formatting
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if text:
                    line_text += text + " "
                    font_sizes.append(span.get("size", 12))
                    font_flags.append(span.get("flags", 0))
            
            # Create content element if line has meaningful text
            if line_text.strip():
                avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12
                
                element = {
                    'text': line_text.strip(),
                    'font_size': avg_font_size,
                    'page': page_number,
                    'type': self._classify_content_type(line_text.strip(), avg_font_size),
                    'formatting': {
                        'bold': any(f & 2**4 for f in font_flags),  # Bold flag
                        'italic': any(f & 2**1 for f in font_flags)  # Italic flag
                    }
                }
                
                elements.append(element)
        
        return elements
    
    def _classify_content_type(self, text, font_size):
        """
        Classify text content into structural types: heading, paragraph, list_item.
        
        This classification logic is intentionally simple and extensible.
        Students can enhance this with machine learning approaches,
        more sophisticated pattern matching, or domain-specific rules.
        """
        
        # Font size based classification (most reliable for digital PDFs)
        if font_size > self.heading_font_threshold:
            self.stats['headings_detected'] += 1
            return 'heading'
        
        # Pattern-based classification for special content types
        list_patterns = [
            r'^\s*[-*+]\s+',           # Bullet lists: -, *, +
            r'^\s*\d+\.\s+',           # Numbered lists: 1., 2., etc.
            r'^\s*\d+\)\s+',           # Numbered lists: 1), 2), etc.
            r'^\s*[a-zA-Z]\.\s+',      # Letter lists: a., b., etc.
            r'^\s*[ivx]+\.\s+',        # Roman numerals: i., ii., etc.
        ]
        
        for pattern in list_patterns:
            if re.match(pattern, text):
                self.stats['list_items_found'] += 1
                return 'list_item'
        
        # Short uppercase text often indicates headings or titles
        if len(text) < 80 and text.isupper() and len(text) > 5:
            self.stats['headings_detected'] += 1
            return 'heading'
        
        # Text ending with colon often indicates section headers
        if len(text) < 100 and text.endswith(':'):
            self.stats['headings_detected'] += 1
            return 'heading'
        
        # Default classification
        self.stats['paragraphs_created'] += 1
        return 'paragraph'
    
    def generate_markdown(self, content_elements):
        """
        Convert structured content elements into well-formatted Markdown.
        
        This method demonstrates how to build structured output from analyzed content.
        The resulting Markdown preserves document hierarchy and improves readability.
        Students can extend this with custom formatting rules or output formats.
        """
        
        if not content_elements:
            return "# Conversion Error\n\nNo content could be extracted from the PDF."
        
        markdown_lines = []
        current_paragraph_lines = []
        heading_counter = {'h1': 0, 'h2': 0, 'h3': 0}
        
        self.log(f"Generating Markdown from {len(content_elements)} content elements")
        
        # Add document header with conversion metadata
        markdown_lines.extend([
            "# Converted Document",
            "",
            f"**Conversion Statistics:**",
            f"- Pages processed: {self.stats['pages_processed']}",
            f"- Content elements: {len(content_elements)}",
            f"- Headings detected: {self.stats['headings_detected']}",
            f"- Paragraphs created: {self.stats['paragraphs_created']}",
            f"- List items found: {self.stats['list_items_found']}",
            "",
            "---",
            ""
        ])
        
        for element in content_elements:
            content_type = element['type']
            text = element['text']
            
            if content_type == 'heading':
                # Flush any accumulated paragraph content before adding heading
                if current_paragraph_lines:
                    paragraph_text = ' '.join(current_paragraph_lines)
                    markdown_lines.append(self._format_paragraph(paragraph_text))
                    markdown_lines.append("")
                    current_paragraph_lines = []
                
                # Determine heading level based on font size and content
                heading_level = self._determine_heading_level(element)
                heading_marker = '#' * heading_level
                
                # Track heading statistics
                heading_key = f'h{heading_level}'
                if heading_key in heading_counter:
                    heading_counter[heading_key] += 1
                
                markdown_lines.append(f"{heading_marker} {text}")
                markdown_lines.append("")
                
            elif content_type == 'list_item':
                # Flush paragraph content before starting list
                if current_paragraph_lines:
                    paragraph_text = ' '.join(current_paragraph_lines)
                    markdown_lines.append(self._format_paragraph(paragraph_text))
                    markdown_lines.append("")
                    current_paragraph_lines = []
                
                # Clean up list item text and format as Markdown list
                clean_text = re.sub(r'^\s*[-*+\d+\.\)\w\.]?\s*', '', text)
                markdown_lines.append(f"- {clean_text}")
                
            else:  # paragraph content
                # Accumulate paragraph lines for better text flow
                current_paragraph_lines.append(text)
        
        # Handle any remaining paragraph content
        if current_paragraph_lines:
            paragraph_text = ' '.join(current_paragraph_lines)
            markdown_lines.append(self._format_paragraph(paragraph_text))
        
        result = '\n'.join(markdown_lines)
        
        self.log(f"Markdown generation complete: {len(result)} characters, {len(markdown_lines)} lines")
        
        return result
    
    def _determine_heading_level(self, element):
        """
        Determine appropriate heading level (1-6) based on font size and content analysis.
        
        This method can be enhanced with more sophisticated document structure analysis.
        For example, tracking heading hierarchy throughout the document or using
        machine learning to detect document patterns.
        """
        font_size = element['font_size']
        text = element['text']
        
        # Font size based levels (most reliable for digital documents)
        if font_size > 20:
            return 1
        elif font_size > 16:
            return 2
        elif font_size > 14:
            return 3
        
        # Content pattern based levels for edge cases
        if any(word in text.lower() for word in ['chapter', 'section', 'part']):
            return 2
        elif len(text) < 30:
            return 3
        else:
            return 3  # Default to h3 for safety
    
    def _format_paragraph(self, text):
        """
        Format paragraph text for better readability in Markdown output.
        
        This method demonstrates text processing techniques that improve
        the final document quality. Students can extend this with more
        sophisticated text cleaning and formatting rules.
        """
        
        # Basic text cleaning
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        # Split very long paragraphs for better readability
        if len(text) > 800:
            sentences = re.split(r'[.!?]+\s+', text)
            if len(sentences) > 2:
                mid_point = len(sentences) // 2
                first_half = '. '.join(sentences[:mid_point]) + '.'
                second_half = '. '.join(sentences[mid_point:])
                return f"{first_half}\n\n{second_half}"
        
        return text
    
    def convert_pdf_to_markdown(self, pdf_path, output_path=None):
        """
        Main conversion method that orchestrates the entire PDF to Markdown process.
        
        This method demonstrates a complete document processing pipeline:
        1. Input validation and setup
        2. Document analysis and structure detection
        3. Content extraction with formatting preservation
        4. Markdown generation and formatting
        5. Output file creation and error handling
        
        Returns True on success, False on failure.
        """
        
        self.log(f"Starting PDF to Markdown conversion: {pdf_path}")
        
        # Validate input file
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found: {pdf_path}")
            return False
        
        # Determine output file path
        if output_path is None:
            pdf_name = Path(pdf_path).stem
            output_path = f"{pdf_name}.md"
        
        self.log(f"Output will be written to: {output_path}")
        
        try:
            # Step 1: Analyze document structure
            analysis = self.analyze_pdf_structure(pdf_path)
            
            if analysis['estimated_type'] == 'error':
                print(f"Error: Cannot process PDF: {analysis.get('error', 'Unknown error')}")
                return False
            
            if analysis['estimated_type'] == 'image_based':
                print("Warning: This appears to be a scanned/image-based PDF.")
                print("Text extraction may be limited. Consider adding OCR capabilities.")
                print("See OCR extension hints in the source code comments.")
            
            # Step 2: Extract structured content
            content_elements = self.extract_structured_content(pdf_path)
            
            if not content_elements:
                print("Error: No text content could be extracted from the PDF.")
                return False
            
            # Step 3: Generate Markdown output
            markdown_content = self.generate_markdown(content_elements)
            
            # Step 4: Write output file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(markdown_content)
            
            # Step 5: Report success with statistics
            file_size = len(markdown_content)
            line_count = len(markdown_content.splitlines())
            
            print(f"Conversion successful!")
            print(f"Output file: {output_path}")
            print(f"Generated {line_count} lines, {file_size} characters")
            print(f"Document analysis: {analysis['estimated_type']} with {analysis['avg_chars_per_page']:.1f} chars/page")
            
            if self.verbose:
                print("\nDetailed Statistics:")
                for key, value in self.stats.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            print("\nThe generated Markdown file is ready for use with document readers,")
            print("note-taking applications, or further processing.")
            
            return True
            
        except Exception as e:
            print(f"Conversion failed: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return False

def setup_command_line_interface():
    """
    Set up command-line argument parsing for user-friendly tool operation.
    
    This function demonstrates how to create professional command-line tools
    that are intuitive for users while providing flexibility for advanced use cases.
    """
    
    parser = argparse.ArgumentParser(
        description=".PDF to .md - Convert PDF documents to Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_to_md.py document.pdf
  python pdf_to_md.py research_paper.pdf --output paper.md
  python pdf_to_md.py complex_doc.pdf --verbose

Educational Notes:
  This tool demonstrates fundamental document processing concepts.
  Extend it with OCR capabilities, web interfaces, or batch processing.
  Perfect foundation for learning about text extraction and format conversion.

OCR Extension:
  For scanned PDFs, add OCR capabilities with tesseract and pdf2image.
  See source code comments for implementation hints.
        """
    )
    
    parser.add_argument(
        'pdf_file',
        help='Path to the PDF file to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output Markdown file path (default: same name as PDF with .md extension)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output for detailed processing information'
    )
    
    return parser

def main():
    """
    Main entry point for the PDF to Markdown conversion tool.
    
    This function demonstrates good practices for command-line tool development:
    - Clear argument parsing and validation
    - Informative help messages
    - Graceful error handling
    - Educational feedback for users
    """
    
    parser = setup_command_line_interface()
    args = parser.parse_args()
    
    # Display tool information
    if args.verbose:
        print(".PDF to .md - Educational PDF to Markdown Converter")
        print("MIT Licensed - Free to use, modify, and distribute")
        print("")
    
    # Initialize converter with user preferences
    converter = PDFToMarkdownConverter(verbose=args.verbose)
    
    # Perform conversion
    success = converter.convert_pdf_to_markdown(args.pdf_file, args.output)
    
    # Provide appropriate exit codes for scripting compatibility
    if success:
        if args.verbose:
            print("\nConversion completed successfully!")
            print("The output file is ready for use with Markdown readers,")
            print("documentation systems, or further text processing.")
        sys.exit(0)
    else:
        print("\nConversion failed. Please check the error messages above.")
        print("For scanned PDFs, consider implementing OCR extensions.")
        sys.exit(1)

if __name__ == "__main__":
    main()

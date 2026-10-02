import markdown
from weasyprint import HTML, CSS

# Read markdown file
with open('docs/SwarmOS_Manual.md', 'r') as f:
    text = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(text, extensions=['extra', 'tables', 'fenced_code', 'toc'])

# Construct full HTML with some styling
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    @page {{
        size: A4;
        margin: 25mm 20mm 25mm 20mm;
        
        @top-left {{
            content: "SwarmOS — Setup & Deployment Manual";
            font-family: Arial, sans-serif;
            font-size: 10pt;
            color: #555;
        }}
        
        @bottom-left {{
            content: "Page " counter(page) " of " counter(pages);
            font-family: Arial, sans-serif;
            font-size: 10pt;
            color: #555;
        }}
    }}
    
    body {{
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        line-height: 1.5;
        color: #333;
        font-size: 11pt;
    }}
    
    h1 {{
        color: #1a5276;
        font-size: 26pt;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
        line-height: 1.2;
    }}
    
    h2 {{
        color: #2980b9;
        font-size: 18pt;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 5px;
        border-bottom: 2px solid #aed6f1;
        text-transform: uppercase;
    }}
    
    h3 {{
        color: #1f618d;
        font-size: 14pt;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 10px;
    }}
    
    p {{
        margin-bottom: 12px;
    }}
    
    code {{
        background-color: #f2f4f4;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: "Courier New", Courier, monospace;
        font-size: 10pt;
        color: #c0392b;
    }}
    
    pre code {{
        display: block;
        padding: 12px;
        background-color: #f8f9f9;
        border: 1px solid #e5e8e8;
        border-radius: 5px;
        overflow-x: auto;
        color: #333;
        font-size: 10pt;
        line-height: 1.4;
        white-space: pre-wrap;
    }}
    
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
        margin-top: 10px;
    }}
    
    th, td {{
        border: 1px solid #d5dbdb;
        padding: 10px;
        text-align: left;
    }}
    
    th {{
        background-color: #ebf5fb;
        color: #1a5276;
        font-weight: bold;
    }}
    
    ul, ol {{
        margin-bottom: 15px;
        padding-left: 25px;
    }}
    
    li {{
        margin-bottom: 5px;
    }}
    
    hr {{
        border: none;
        border-top: 2px solid #2c3e50;
        margin: 30px 0;
    }}
    
    strong {{
        color: #2c3e50;
    }}
    
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

# Render PDF
HTML(string=html).write_pdf(
    '/home/priyanshu/Documents/SwarmOS_Complete_Replication_Setup_Deployment_Manual.pdf'
)
print("PDF generated successfully.")

<h1 align="center">Bumpas portfolio and blog</h1>
<p align="center">Astro and modified theme from Northendlab. Added a small photography page to display a few selects.</p>

---

<h2 align="center"> <a target="_blank" href="https://northendlab-light-astro.vercel.app/" rel="nofollow">👀Demo</a> | <a  target="_blank" href="https://pagespeed.web.dev/report?url=https%3A%2F%2Fnorthendlab-light-astro.vercel.app%2F&form_factor=desktop">Page Speed (100%)🚀</a>
</h2>

<p align=center>
  <a href="https://github.com/withastro/astro/releases/tag/astro%405.5.2" alt="Contributors">
    <img src="https://img.shields.io/static/v1?label=ASTRO&message=5.5&color=000&logo=astro" />
  </a>

  <a href="https://github.com/themefisher/northendlab-light-astro/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/themefisher/northendlab-light-astro" alt="license"></a>

  <img src="https://img.shields.io/github/languages/code-size/themefisher/northendlab-light-astro" alt="code size">

  <a href="https://github.com/themefisher/northendlab-light-astro/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/themefisher/northendlab-light-astro" alt="contributors"></a>
</p>

![northendlab-light](https://demo.gethugothemes.com/thumbnails/northendlab-light.png)

## 🔑Key Features

- 📄 10+ Pre-designed pages
- 🎨 Highly Customizable (Color, Font, Menu, Social Links, SEO Meta Tags, etc.)
- ⚡ Fast by Default (95+ Google PageSpeed Score)
- ⚙️ Netlify Settings Pre-configured
- 📬 Contact Form Support
- 🌅 Support OG Image
- ✍️ Write and Update Content in Markdown / MDX
- 📚 MDX Components Auto Import
- 📝 Includes Draft Pages and Posts
- 🎨 Built with Tailwind CSS Framework
- 📱 Fully Responsive on Desktops, Tablets, and Smartphones
- 🔍 SEO Friendly

## 📄 10+ Pre-designed pages

- 🏠 Home Page
- 👤 About
- 📞 Contact
- 🔒 Privacy Policy Page
- 📝 Blog Pages
- 📄 Blog Single Pages
- 👤 Author Page
- 👤 Author Single Page
- 🗂️ Category Page
- 📄 Category Single Page

<!-- installation -->

## ⚙️Installation

After downloading the template, you have some prerequisites to install. Then you can run it on your localhost. You can view the package.json file to see which scripts are included.

### 🔧Install prerequisites (once for a machine)

- **Node Installation:** [Install node js](https://nodejs.org/en/download/) [Recommended LTS version]

### 🖥️Local setup

After successfully installing those dependencies, open this template with any IDE [[VS Code](https://code.visualstudio.com/) recommended], and then open the internal terminal of IDM [vs code shortcut <code>ctrl/cmd+\`</code>]

- Install dependencies

```
npm install
```

- Run locally

```
npm run dev
```

After that, it will open up a preview of the template in your default browser, watch for changes to source files, and live-reload the browser when changes are saved.

## 🔨Production Build

After finishing all the customization, you can create a production build by running this command.

```
npm run build
```

## 📄 Resume (ATS) PDF generation

This repo includes an ATS-friendly resume generator. The ATS version avoids special glyphs and complex layouts so parsers can read it reliably.

Output location:

- `Andrew-Bumpas-Resume-ATS.pdf`

Generate the PDF:

```
python3 scripts/generate_resume_pdf.py
```

Or via npm:

```
npm run resume
```

Optional (first time): install the ReportLab dependency if not already present.

```
python3 -m pip install --user reportlab
```

You can control the source and starting line (1-based) via CLI or environment variables:

```
# CLI flags
python3 scripts/generate_resume_pdf.py \
  --source /absolute/path/to/-index.md \
  --start-line 14 \
  --header "ANDREW BUMPAS"

# Or with environment variables
ATS_SOURCE_MD=/absolute/path/to/-index.md ATS_START_LINE=14 ATS_HEADER="ANDREW BUMPAS" \
  python3 scripts/generate_resume_pdf.py
```

By default, the generator reads from the About page:
`src/content/about/-index.md` starting at line 14.

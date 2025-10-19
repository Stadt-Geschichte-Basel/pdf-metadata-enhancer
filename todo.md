# TODO Tracking

This file tracks all TODO items identified in the repository during initialization.

## ✅ Completed TODOs

### From README.template.md (now completed in README.md)

- ✅ **Replace REPO_NAME**: Changed to `pdf-metadata-enhancer`
- ✅ **Replace USERNAME**: Changed to `Stadt-Geschichte-Basel`
- ✅ **Replace FULLNAME**: Changed to `Moritz Mähr`
- ✅ **Replace SHORT_DESCRIPTION**: Changed to "Tools and workflows for enhancing PDF metadata for digital preservation and accessibility"
- ✅ **Replace [INSERT CONTACT METHOD]**: Changed to `info@stadtgeschichtebasel.ch`
- ✅ **Update Data Description section**: Replaced generic TODO placeholders with PDF metadata-specific content
- ✅ **Update all repository URLs**: Updated GitHub links throughout configuration files
- ✅ **Format all files**: Applied Prettier formatting
- ✅ **Install dependencies**: Ran `npm install` and `npm run prepare`
- ✅ **Finalize README**: Deleted template README and activated project-specific version

### Recent Additions (October 2025)

- ✅ **Add SGB Dataset**: Added `sgb/dois.txt` with 88 DOIs from Stadt-Geschichte-Basel catalog
- ✅ **Add SGB Metadata**: Created `sgb/metadata.json` with pre-fetched CSL-JSON metadata
- ✅ **Create DOI Harvester Script**: Implemented `src/scripts/get_metadata.py` for automated DOI extraction and metadata fetching
- ✅ **Document SGB Dataset**: Updated README.md with SGB dataset documentation
- ✅ **Document Helper Scripts**: Added comprehensive documentation for get_metadata.py
- ✅ **Update Project Structure**: Documented the sgb/ directory and scripts/ directory in README.md

## 📋 Open TODOs

### From README.md (Zenodo Integration)

- [ ] **Replace GITHUB_REPO_ID**: Line 10 - Replace with actual GitHub repository ID from `https://api.github.com/repos/Stadt-Geschichte-Basel/pdf-metadata-enhancer`
- [ ] **Replace ZENODO_RECORD**: Multiple lines (36-44, 49) - Replace with actual Zenodo DOI record ID once repository is archived on Zenodo

### From Repository Files

- [ ] **documentation/codelist.txt**: Line 1 - Complete URL reference: "TODO https://ec.europa.eu/eurostat/web/metadata/code-lists"
- [ ] **.gitattributes**: Line with "TODO text" - Define proper text attribute handling
- [ ] **report.md**: Contains `<!-- TODO -->` placeholder - Need to add actual report content
- [ ] **project-management/project-report.md**: Contains `<!-- TODO -->` placeholder
- [ ] **project-management/communication.md**: Contains `<!-- TODO -->` placeholder
- [ ] **project-management/tools.md**: Contains `<!-- TODO -->` placeholder
- [ ] **project-management/people.md**: Contains `<!-- TODO -->` placeholder

### Optional Setup Tasks (from original README checklist)

- [ ] **Enable GitHub Security Alerts**: Go to repository "Security" tab and enable alerts
- [ ] **Protect Main Branch**: Set up branch protection rules in repository settings
- [ ] **Set Up Zenodo Integration**: Connect repository to Zenodo for DOI generation
- [ ] **Enable GitHub Pages**: Configure Pages to publish from `gh-pages` branch
- [ ] **Publish Documentation**: Run `quarto publish gh-pages` to publish documentation
- [ ] **Add Citation File**: Create `CITATION.cff` file ✅ **COMPLETED** - Created with project-specific metadata based on template
- [ ] **Add Zenodo Metadata File**: Create `.zenodo.json` for Zenodo metadata (optional)
- [ ] **Add Favicons**: Repository already has favicons, but may need customization

## 📝 Notes

- **Zenodo Integration**: The ZENODO_RECORD placeholders should be replaced after setting up Zenodo archiving for the repository
- **GitHub Repository ID**: Can be obtained from GitHub API: `curl https://api.github.com/repos/Stadt-Geschichte-Basel/pdf-metadata-enhancer`
- **Documentation TODOs**: The project-management folder contains template files that need content specific to this project
- **Repository Setup**: Some tasks require administrative access to GitHub repository settings

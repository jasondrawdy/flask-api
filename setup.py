from setuptools import setup, find_packages
import datetime
import codecs
import os

class Egg:
    """A encapsulation object containing all necessary components for creating a pip package."""
    def __init__(self: "Egg") -> None:
        self.package = "Flask API"
        self.author = "Jason Drawdy"
        self.email = "enter_your_email_at@email.com"
        self.website = "https://www.youremailhere.com"
        self.references = {
            "Documentation": "put_a_docs_link_here",
            "Issue Tracker": "put_an_issues_link_here"
        }
        self.version = '0.0.0'
        self.description = 'Short description of project here...'
        self.long_description = self._get_project_readme()

    def _get_project_readme(self: "Egg"):
        """Returns the current README documentation or a default description."""
        default_data = 'Description to use if no README file is found here...'
        current_path = os.path.abspath(os.path.dirname(__file__))
        readme_file = os.path.join(current_path, "README.md")
        if os.path.exists(readme_file):
            with codecs.open(readme_file, encoding="utf-8") as file:
                return file.read()
        return default_data 

    def prepare_for_archiving(self: "Egg"):
        """Temporarily modifies the current project structure for more accurate packaging."""
        os.rename('src', self.package)

    def restore_original_structure(self: "Egg"):
        """Creates the original file and directory structure before the creation of any packages."""
        os.rename(self.package, 'src')
    
    def create_project_package(self: "Egg"):
        """Performs the actual package creation process using all provided `setup()` function information."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
        self.long_description += f"\n\nBuilt by {self.author} — {timestamp}"
        try:
            setup(
                name=self.package,
                version=self.version,
                author=self.author,
                author_email=self.email,
                description=self.description,
                long_description_content_type="text/markdown",
                long_description=self.long_description,
                url=self.website,
                project_urls=self.references,
                packages=find_packages(),
                keywords=['add', 'your', 'keywords', 'here'],
                classifiers=[
                    "Development Status :: 3 - Alpha",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: MIT License",
                    "Programming Language :: Python :: 3.6",
                    "Programming Language :: Python :: 3.7",
                    "Programming Language :: Python :: 3.8",
                    "Programming Language :: Python :: 3.9",
                    "Programming Language :: Python :: 3.10",
                    "Programming Language :: Python :: 3.11",
                    "Operating System :: OS Independent",
                ]
            )
        except: pass # Cleanup will be called after setup.

package = Egg()
package.prepare_for_archiving()
package.create_project_package()
package.restore_original_structure()
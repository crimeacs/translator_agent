# Translation Agent: Advanced PDF Linguistic Converter

Welcome to the Translation Agent, an advanced linguistic conversion tool designed to seamlessly extract, translate, and consolidate content from PDF documents. This sophisticated utility leverages OpenAI's GPT model to provide accurate translations, generating a professional certificate of translation and merging the translated text with the original document into a comprehensive file.

## Core Features

- **Robust Text Extraction**: Efficiently pulls text from any PDF document.
- **Intelligent Translation**: Utilizes OpenAI's cutting-edge GPT model for high-quality translations.
- **PDF Generation**: Creates a PDF document of the translated text.
- **Certificate of Translation**: Automatically generates a verifiable certificate of translation.
- **PDF Merging**: Combines the original and translated PDFs into a single document for easy reference.

## Installation

Ensure you have Python installed on your system. Then, install the necessary dependencies with the following command:

```bash
pip install -r requirements.txt
```

## How to Use

Execute the script from the command line, providing the necessary parameters:

```bash
python extract_and_translate.py --pdf_path "path/to/input.pdf" --output "path/to/output.pdf" --api_key "your-openai-api-key" --name "Your Name" --address "Your Address" --language_1 "Source Language" --language_2 "Target Language" --certificate_output "path/to/certificate.pdf"
```
## Sample script

```bash
python extract_and_translate.py --pdf_path 'sample.pdf' --output 'test.pdf' --api_key '<YOUR-API-KEY>' --name 'Markus Avrelius' --address '1111 Madeup st, MadeupTown, 94117, CA' --language_1 'Russian' --language_2 'English' --certificate_output 'test_certificate.pdf'
```

### Command-Line Arguments

- `--pdf_path`: The path to the input PDF file.
- `--output`: The desired path for the output merged PDF file.
- `--api_key`: Your OpenAI API key for translation services.
- `--name`: The name to be printed on the certificate of translation.
- `--address`: The address to be included on the certificate of translation.
- `--language_1`: The source language of the original document.
- `--language_2`: The target language for the translation.
- `--certificate_output`: The file path for the generated certificate of translation PDF.

## Contributing

We welcome contributions from the community! If you'd like to contribute to the Translation Agent, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Develop your changes in your branch.
4. Ensure your code adheres to the existing style of the project to maintain consistency.
5. Write or adapt tests as needed.
6. Submit a pull request with a clear description of your changes.

## Licensing

For more details, please refer to the LICENSE file.

## Support

For support, feature requests, or contributions, please open an issue in the project's GitHub repository.
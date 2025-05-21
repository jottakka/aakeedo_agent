

# Ākēdo Kanji (アアケード漢字) AI Agent Toolkit

  

This agent is aimed to help Japanese learners improve their knowledge about Kanjis. It currently uses the [https://kanjiapi.dev/](https://kanjiapi.dev/) API and also the WaniKani API (primarily for retrieving basic user data at the moment).

  

In the future, it can be expanded to leverage more features from both Kanji API and WaniKani's learning system to offer a more personalized learning experience.

  This agent is built using the [Arcade AI toolkit](https://docs.arcade.dev/)

## Features
### Available Tools


  **get_user_information**: Fetches the WaniKani username and current WaniKani level for the user.

       Requires a WaniKani API token (configured as an Arcade secret)._

       Input: None

       Output: JSON string with user data (username, level) on success, or an error message on failure._

**get_kanji_details:** Retrieves detailed information for a specific Japanese kanji character (e.g., stroke count, grade, meanings, readings).

    Input: A single kanji character.
    
    Output: JSON string with kanji details.
  

**list_joyo_kanji:** Fetches the complete list of Jōyō (officially recognized, commonly used) kanji characters.

    Input: None.
    
    Output: JSON string array of Jōyō kanji.


**get_kanji_list_by_category:** Fetches a list of kanji based on a specified category (e.g., 'joyo', 'jinmeiyo', 'grade-1', 'jlpt-n1').

    Input: Category name string.
    
    Output: JSON string array of kanji for that category.

  

**get_kanji_by_reading:** Fetches kanji associated with a given Japanese reading (in hiragana or katakana).

    Input: Reading string (e.g., 'みつ', 'ニチ').
    
    Output: JSON string with the reading and associated main/name kanji.
    
    
   **get_words_for_kanji:** Fetches a list of dictionary word entries that use a specific kanji character.

    Input: A single kanji character.
    
    Output: JSON string array of word entries (including readings and meanings).



## Tests and Evals


### Tests

  

The `tests/` directory contains automated tests:

  

* **`tests/http_clients/test_wanikani_api_http_client.py`**: *(Tests WaniKani API client functionality.)*

* **`tests/test_kanji_api_http_client.py`**: *(Tests KanjiAPI client functionality.)*

* **`tests/test_kanji_api_tools.py`**: *(Tests tools using the KanjiAPI.)*

  

### Evals

There are simple evals available to validate the tools perfromance:
  

The `evals/` directory is for agent performance assessment:

  

* **`evals/eval_aakeedo_kanji.py`**: *(Evaluates specific agent tasks or overall effectiveness.)*


## Setting the WaniKani API Token

### 1. Arcade AI Cloud Environment

In the Arcade AI platform, you should store your WaniKani API token as a **secret environment variable**. This allows your application to securely access the token without exposing it in the code or configuration files.

- **Secret name:** `WANIKANI_API_TOKEN`  
- **Value:** Your personal WaniKani API token (you can get it from your WaniKani account settings)

Make sure to add this secret in your Arcade project environment settings before running your agent.

## Environment Variables (`.env` file) Configuration

The `AakeedoConfig` Python class reads configuration values from environment variables, which you can conveniently set in a `.env` file during local development. Below are the key variables you should define in your `.env` file to match the config class:

| Environment Variable       | Description                                                                                 | Default Value                      |
|---------------------------|---------------------------------------------------------------------------------------------|----------------------------------|
| `KANJI_API_BASE_URL`       | Base URL for the Kanji API. Overrides the default `"https://kanjiapi.dev/v1"` endpoint.     | `https://kanjiapi.dev/v1`         |
| `WANIKANI_API_BASE_URL`    | Base URL for the WaniKani API v2.                                                          | `https://api.wanikani.com/v2/`    |
| `WANIKANI_API_REVISION`    | Revision date required in WaniKani API request headers.                                     | `20170710`                       |
| `WANIKANI_API_TOKEN`       | Your personal WaniKani API token for authenticated API access. **This is required for local tests**.        | *(no default — must be provided)*| 

### Example `.env` file

```env
KANJI_API_BASE_URL=https://kanjiapi.dev/v1
WANIKANI_API_BASE_URL=https://api.wanikani.com/v2/
WANIKANI_API_REVISION=20170710
WANIKANI_API_TOKEN=your-wanikani-api-token-here
```
## Install

  

Install this toolkit using pip:

```bash

pip install arcade_aakeedo_kanji

```

For further instruction related to deployment and local testing visit : https://docs.arcade.dev/home

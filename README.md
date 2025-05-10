# Public APIs Category Search (React Package)

This is a React package that allows you to easily search and retrieve a list of public APIs categorized by different topics. It provides a simple function to get a list of APIs belonging to a specific category from a curated list.

## Installation

You can install this package using npm:
```
bash
npm install @supunlakmal/public-apis
```
*(Replace `your-package-name` with the actual name you will use when publishing)*

## Usage

The package exports a single function, `getApisByCategory`, which takes a category name as a string and returns an array of API objects for that category.
```
javascript
import { getApisByCategory } from 'your-package-name';

// Example usage in a React component or other JavaScript file
const animalApis = getApisByCategory('Animals');

console.log(animalApis);
/*
  Example output (structure may vary slightly based on the actual JSON data):
  [
    {
      name: "Cat Facts",
      description: "Daily cat facts",
      auth: "",
      https: true,
      cors: "yes",
      link: "https://catfact.ninja/"
    },
    // ... more animal APIs
  ]
*/

const animeApis = getApisByCategory('Anime');
console.log(animeApis);
```
The function will return an empty array if the category is not found.

## Scripts

This package includes the following npm scripts for development and publishing:

*   `npm run build`: Compiles the TypeScript code using the `tsc` command.
*   `npm run format`: Formats the code using Prettier.
*   `npm run p`: Publishes the package to npm with public access.


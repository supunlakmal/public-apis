import apiData from './categorized_apis_from_readme.json';

/**
 * Interface for an individual API entry.
 */
interface Api {
  name: string;
  description: string;
  auth: string;
  https: boolean;
  cors: string;
  link: string;
}

/**
 * Returns a list of APIs belonging to a specific category.
 *
 * @param category The category name to filter by.
 * @returns An array of Api objects or an empty array if the category is not found.
 */
export function getApisByCategory(category: string): Api[] {
  // The original code `if (apiData && apiData[category])` implies two checks:
  // 1. `apiData` itself is truthy (not null/undefined).
  // 2. The looked-up property `apiData[category]` is truthy.

  // First, handle the case where `apiData` might be null or undefined.
  // For a static JSON import, `apiData` is generally guaranteed to be the parsed object,
  // but preserving this check from the original logic is safer.
  if (!apiData) {
    return [];
  }

  // `apiData` is now known to be truthy (i.e., an object).
  // To safely access a property using a dynamic string `category`, we cast `apiData`
  // to a type that explicitly allows string indexing. `Record<string, Api[] | undefined>`
  // means it's an object where keys are strings, and values are either `Api[]` or `undefined`.
  const typedApiDataObject = apiData as Record<string, Api[] | undefined>;

  // Access the property using the category string.
  // `apisForCategory` will be of type `Api[] | undefined`.
  const apisForCategory = typedApiDataObject[category];

  // If `apisForCategory` is truthy (i.e., it's an array, not undefined),
  // it means the category exists and has APIs.
  // TypeScript's control flow analysis will narrow the type of `apisForCategory` to `Api[]` here.
  if (apisForCategory) {
    return apisForCategory; // No need for `as Api[]` cast, type is correctly narrowed.
  }

  // If the category is not found or `apiData` was falsy, return an empty array.
  return [];
}
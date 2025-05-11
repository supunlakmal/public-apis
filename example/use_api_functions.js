// example/example_usage.js

import { getApisByCategory, searchApis, getAllApis } from '../src/index.js';

// Example using getApisByCategory
console.log('--- APIs in Cryptocurrency category ---');
const cryptoApis = getApisByCategory('Cryptocurrency');
if (cryptoApis.length > 0) {
  cryptoApis.forEach(api => {
    console.log(`- ${api.name}: ${api.description}`);
  });
} else {
  console.log('No APIs found in the Cryptocurrency category or category does not exist.');
}

console.log('\n--- APIs matching "Dungeons" query ---');
// Example using searchApis
const dungeonApis = searchApis('Dungeons');
if (dungeonApis.length > 0) {
    dungeonApis.forEach(api => {
        console.log(`- ${api.name}: ${api.description}`);
    });
} else {
    console.log('No APIs found matching the query "Dungeons".');
}

console.log('\n--- All APIs ---');
// Example using getAllApis
const allApis = getAllApis();
if (allApis.length > 0) {
    console.log(`Total number of APIs: ${allApis.length}`);
    // You can optionally log details of a few APIs
    // allApis.slice(0, 5).forEach(api => {
    //     console.log(`- ${api.name}`);
    // });
} else {
    console.log('No APIs found.');
}
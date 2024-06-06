const fs = require('fs');

// Script to update the ad CSS selectors file (used internally to detect ads)
// with the latest definitions from Easylist.

fetch('https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_general_hide.txt').then(res => {
  if (!res.ok) {
    console.log(res.statusText);
    process.exit(1);
  }
  return res.text();
}).then(raw => {
  const rows = raw.split('\n');
  const selectorRows = rows
      .filter(r => r.startsWith('##'))
      .map(row => row.substring(2).replace(/"/g, '\\"'));
    //   .map(row => console.log(row.substring(2)));

  let towrite = 'const selectors = [\n';
  
  let selectors = selectorRows.join('",\n"');
//   selectors.replace(/"/g, "\"");
//   selectors.replace(/,/g, "",\n"");
  selectors = '"' + selectors + '"';

  let res = towrite.concat(selectors);
  let res1 = res.concat('\n]\;\nmodule.exports = selectors;')
  fs.writeFileSync('./easylist_selectors_update.js', res1);
  console.log('Success - Wrote new selectors to src/ads/easylist_selectors.json');
});

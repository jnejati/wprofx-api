const CDP = require('chrome-remote-interface');
const  readline = require('readline');
const fs = require('fs');
const options = {local:'true'};

var TRACE_CATEGORIES = ["-*", "toplevel", "blink.console", "disabled-by-default-devtools.timeline", "devtools.timeline", "disabled-by-default-devtools.timeline.frame", "devtools.timeline.frame","disabled-by-default-devtools.timeline.stack", "disabled-by-default-v8.cpu_profile",  "disabled-by-default-blink.feature_usage", "blink.user_timing", "v8.execute", "netlog"];

//var sites_list = './config/testsites.txt';
var myArgs = process.argv.slice(2);
var _url = myArgs[0];
var tracefile = myArgs[1];

CDP(options, async (client) => {
    try {
        const {Page, Network, Tracing} = client;
        // enable Page domain events
        await Page.enable();
        await Network.enable();
        await Network.setCacheDisabled;
        await Network.clearBrowserCache();
        await Network.clearBrowserCookies();
        // trace a page load
        const events = [];
        await Tracing.dataCollected(({value}) => {
            events.push(...value);
        });
        await Tracing.start({ "categories":   TRACE_CATEGORIES.join(',')});
        await Page.navigate({url: _url});
        await Page.loadEventFired();
        await Tracing.end();
        await Tracing.tracingComplete();
        // save the tracing data
        fs.writeFileSync(tracefile + '.json', JSON.stringify(events));
        await client.close();
    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
    }
   }).on('error', (err) => {
    console.error(err);
   });

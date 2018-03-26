'use strict';
console.log('Loading function');

exports.handler = (event, context, callback) => {
    console.log('Hello World (Node edition)!');
    callback(null, 'Hello World (Node edition)!');
};
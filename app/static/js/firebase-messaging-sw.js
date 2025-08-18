importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyCHRHQfuw81Cs1u8I5ep5PLJs3OuSsKaMY",
    authDomain: "ou-library.firebaseapp.com",
    projectId: "ou-library",
    storageBucket: "ou-library.firebasestorage.app",
    messagingSenderId: "739534297897",
    appId: "1:739534297897:web:d4a55b6044d2b31a2d3538",
    measurementId: "G-XQ1X2C5CBJ"
});

const messaging = firebase.messaging();


/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
/*var stripe_public_key = 'pk_test_51K0ZuLGc2X9Nm4M2l45fWyPvOUNhNfwIvHdIQV2hCcc9uxdBwjRciYsIpUW8KX42QdGdXc9viedqGEF1PBF6GRQ8004qOoKrSs'*/
/*var client_secret = 'sk_test_51K0ZuLGc2X9Nm4M21aXjR765tUUCNaMyL6CEbVILac15e9plRiszP25DExP0vifSijVkdXD3FLknq0GnD5JjeOoT00QH0dyqT7';*/
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');
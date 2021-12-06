/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
/*var stripe_public_key = 'pk_test_51K0ZuLGc2X9Nm4M2l45fWyPvOUNhNfwIvHdIQV2hCcc9uxdBwjRciYsIpUW8KX42QdGdXc9viedqGEF1PBF6GRQ8004qOoKrSs'*/
/*var client_secret = 'sk_test_51K0ZuLGc2X9Nm4M21aXjR765tUUCNaMyL6CEbVILac15e9plRiszP25DExP0vifSijVkdXD3FLknq0GnD5JjeOoT00QH0dyqT7';*/
var stripe = Stripe(stripePublicKey);
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

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});



//
//When the user clicks the submit button the event listener prevents the form from submitting
//and instead disables the card element and triggers the loading overlay.
//Then we create a few variables to capture the form data we can't put in
//the payment intent here, and instead post it to the cache_checkout_data view
//The view updates the payment intent and returns a 200 response, at which point we
//call the confirm card payment method from stripe and if everything is ok
//submit the form.
//If there's an error in the form then the loading overlay will
//be hidden the card element re-enabled and the error displayed for the user.
//If anything goes wrong posting the data to our view. We'll reload the page and
//display the error without ever charging the user.
//
//

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    console.log('submit called')
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    console.log('submit called')
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    console.log('saveinfo')
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    console.log('csrfToken')

    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    console.log('postData');

    var url = '/checkout/cache_checkout_data/';
    console.log('posting');
    
    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
            console.log('stripe error');
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    console.log('stripe success')
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        console.log('submit fail')
        location.reload();
    })
});
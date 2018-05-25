'use strict';

$('.copy-button').on('click', () => {
  document.getElementsByClassName('copy-link')[0].select();
  document.execCommand('copy');
});

$('.sound-listing-text').on('click', 'input', function() {
  this.select();
  document.execCommand('copy');
});

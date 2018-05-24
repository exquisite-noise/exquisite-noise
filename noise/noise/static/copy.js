'use strict';

$('.copy-button').on('click', () => {
  $('.copy-link').select();
  document.execCommand('copy');
});

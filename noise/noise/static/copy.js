'use strict';

$('.copy-button').on('click', () => {
  document.getElementsByClassName('copy-link')[0].select();
  document.execCommand('copy');
});

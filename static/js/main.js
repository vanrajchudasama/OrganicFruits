

 $('#rat1').click(function() {
  $('#rat4').removeClass('text-success');
  $('#rat5').removeClass('text-success');
  $('#rat3').removeClass('text-success');
  $('#rat2').removeClass('text-success');
  $('#rat2').removeClass('text-warning');

  $('#rat4').removeClass('text-secondary');
  $('#rat5').removeClass('text-secondary');
  $('#rat3').removeClass('text-secondary');
  $('#rat2').removeClass('text-secondary');

  $('#rat1').toggleClass('text-danger')
  document.getElementById('rating').value='1'

 });
 $('#rat2').click(function() {
  $('#rat1').removeClass('text-danger');

  $('#rat4').removeClass('text-success');
  $('#rat5').removeClass('text-success');
  $('#rat3').removeClass('text-success');

  $('#rat1').addClass('text-warning');
  $('#rat2').toggleClass('text-warning');
  document.getElementById('rating').value='2'

 });
 $('#rat3').click(function() {
  $('#rat1').removeClass('text-warning');
  $('#rat1').removeClass('text-danger');

  $('#rat2').removeClass('text-warning');

  $('#rat4').removeClass('text-success');
  $('#rat5').removeClass('text-success');

  $('#rat1').addClass('text-success');
  $('#rat2').addClass('text-success');
  $('#rat3').toggleClass('text-success');
  document.getElementById('rating').value='3'

 });
 $('#rat4').click(function() {

  $('#rat5').removeClass('text-success');
  $('#rat1').removeClass('text-danger');


  $('#rat1').addClass('text-success');
  $('#rat2').addClass('text-success');
  $('#rat3').addClass('text-success');
  $('#rat4').toggleClass('text-success');
  document.getElementById('rating').value='4'

 });
 $('#rat5').click(function() {
  $('#rat1').removeClass('text-danger');
  $('#rat1').removeClass('text-warning');
  $('#rat2').removeClass('text-warning');

  $('#rat1').addClass('text-success');
  $('#rat2').addClass('text-success');
  $('#rat3').addClass('text-success');
  $('#rat4').addClass('text-success');
  $('#rat5').toggleClass('text-success');
  document.getElementById('rating').value='5'


 });

//  -------------------------------------------review js----------------------


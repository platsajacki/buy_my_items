export async function applyCoupon() {
  const couponCode = document.getElementById('coupon-id').value.toLocaleLowerCase()
  fetch('/purchases/coupons/' + couponCode + '/')
    .then(
      response => {
        if (response.ok) {return response.json()}
      }
    )
    .then(
      data => {
        document.getElementById('coupon-id').value = data.id
        document.getElementById('coupon-id').style.color = 'green'
        document.getElementById('percent-off').value = data.percent_off
        alert('Coupon applied successfully!')
      }
    )
    .catch(
      error => {alert('Error applying coupon: ' + error.message)}
    )
}

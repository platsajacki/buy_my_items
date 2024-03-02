const buyForm = document.querySelector('.buy-form')


function checkСurrencySelectedItems(event) {
  const selectedItems = document.querySelectorAll('input[name="items"]:checked')
  let currencies = new Set()
  selectedItems.forEach(
    item => {currencies.add(item.getAttribute('currency').trim())}
  )
  if (currencies.size > 1) {
    alert('You can only pay for the product in one currency.')
    event.preventDefault()
  }
  if (currencies.size === 0) {
    alert('Select items.')
    event.preventDefault()
  }
}


buyForm.addEventListener('submit', checkСurrencySelectedItems)

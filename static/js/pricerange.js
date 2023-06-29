const minInput = document.querySelector("#min_input");
const minValue = document.querySelector("#min_value");

minValue.textContent = minInput.value;
minInput.addEventListener("input", (event) => {
  minValue.textContent = event.target.value;
});

const maxInput = document.querySelector("#max_input");
const maxValue = document.querySelector("#max_value");

maxValue.textContent = maxInput.value;
maxInput.addEventListener("input", (event) => {
  maxValue.textContent = event.target.value;
});
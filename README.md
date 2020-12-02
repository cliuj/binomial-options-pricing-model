# Binomial Option Pricing Model (CRR Model)

## About
This repository contains the follow report project submitted for Math 3332 - Probability and Inference.

## Report
The report in this repository is the `binomial_pricing_model.tex` and was compiled with `XeLatex`.

**Note:** Other versions of Latex might work, but have not been tested.

## Application
Along with the report, an application titled `binomial_options_pricing_model.py` was written in `Python3`.
The inputs for this program can be configured with different inputs in the form of a `dictionary`.

An example of the configuration format:
```
inputs = {
        "option_style": "american",
        "option_type": "call",
        "stock_price": 100,
        "strike_price": 120,
        "volatility": 0.316,
        "risk_free_interest_rate": 0.0009,
        "up_factor": 1.25,
        "down_factor": 0.80,
        "T": 1,
        "time_periods": 2 
    }
```
can be found in the same program file.

## Example output
![alt text](https://github.com/cliuj/binomial-options-pricing-model/blob/staging/images/bopm_output_screenshot.png)

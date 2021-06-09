def get_title(title, model_cfg, hurst, bjl, params, std_price, std_returns, norm):
    title = '<b>'+title+'</b>'+'<br>CFG:' + str(model_cfg)
    title += '<br>HURST EXPONENT: ' + str(round(hurst, 4))
    title += ' , Price Std: ' + str(round(std_price, 2))
    title += ' , Returns Std: ' + str(round(std_returns, 4))
    title += ' , Box-Ljung Test: ' + str(round(bjl, 4))
    title += ' , Normality Test: ' + str(round(norm, 4))
    omega, alpha, beta = params['omega'], params['alpha[1]'], params['beta[1]']
    title += " , GARCH MODEL: &#963;<sup>2</sup><sub>t</sub> = {:.3} + {:.3} &#949;<sup>2</sup><sub>t</sub> + {" \
             ":.3} &#963;<sup>2</sup><sub>t-1</sub>".format(omega, alpha, beta)

    return title

// @ts-check

(() => {
  /**
   * @param {Function} handler
   * @param {Function} condition
   * @param {number} delay
   * @param {number} retry
   * @param {...any} args
   * @returns {Promise<any>}
   */
  const retryAsync = (handler, condition, delay, retry, ...args) => {
    return new Promise((resolve, reject) => {
      let tryCnt = 0;
      const handlerWrapper = () => {
        tryCnt++;
        if (tryCnt - 1 > retry) {
          reject(new Error(`OverMaxRetryCountError(${retry} time(s))`));
          return;
        }

        console.log(`trying ${tryCnt} time(s)`);

        const result = handler(...args);
        if (condition(result)) {
          console.log("succeeded");

          resolve(result);
        } else {
          console.log("failed");

          setTimeout(handlerWrapper, delay * 1000);
        }
      };
      handlerWrapper();
    });
  };

  const querySelectorWrapper = selectors => {
    return document.querySelector(selectors);
  };

  const querySelectorAllWrapper = selectors => {
    return document.querySelectorAll(selectors);
  };

  const notNull = result => {
    return result !== null;
  };

  const notZeroLength = resultArray => {
    return resultArray.length > 0;
  };

  const querySelector2 = (selectors, delay = 2, retry = 5) => {
    return retryAsync(querySelectorWrapper, notNull, delay, retry, selectors);
  };

  const $2 = querySelector2;

  const querySelectorAll2 = (selectors, delay = 2, retry = 5) => {
    return retryAsync(
      querySelectorAllWrapper,
      notZeroLength,
      delay,
      retry,
      selectors
    );
  };

  const $$2 = querySelectorAll2;

  const addTgt2 = () => {
    const newNode = document.createElement("div");
    newNode.className = "tgt2";
    newNode.textContent = "tgt2";
    document.body.append(newNode);
  };

  Document.prototype.$2 = $2;
  Document.prototype.$$2 = $$2;

  window.setTimeout(addTgt2, 5000);

  const observer = new MutationObserver(records => {
    console.log("mutated");
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
})();

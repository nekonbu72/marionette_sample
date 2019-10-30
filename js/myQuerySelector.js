// @ts-check

/**
 * @param {Function} handler
 * @param {Function} condition
 * @param {number} delay
 * @param {number} retry
 * @param {...any} args
 * @returns {Promise<any>}
 */
const intervalAsync = (handler, condition, delay, retry, ...args) => {
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
  return intervalAsync(querySelectorWrapper, notNull, delay, retry, selectors);
};

const $2 = querySelector2;

const querySelectorAll2 = (selectors, delay = 2, retry = 5) => {
  return intervalAsync(
    querySelectorAllWrapper,
    notZeroLength,
    delay,
    retry,
    selectors
  );
};

const $$2 = querySelectorAll2;

const addElm = () => {
  const newNode = document.createElement("div");
  newNode.className = "tgt2";
  newNode.textContent = "tgt2";
  document.body.append(newNode);
};

window.setTimeout(addElm, 7000);

$2(".tgt3")
  .then(res => console.log("result: ", res))
  .catch(e => console.error(e));

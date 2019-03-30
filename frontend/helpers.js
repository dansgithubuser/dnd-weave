export default {
  arrayResize: function (array, size, construct) {
    if (size < array.length) {
      const d = array.length - size;
      array.splice(-d, d);
    } else {
      array.push(...Array.from({ length: size - array.length }, construct))
    }
  },
}

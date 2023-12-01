// store.js

import { createStore } from 'vuex';

export default createStore({
  state: {
    uploadData: null,
  },
  mutations: {
    setUploadData(state, data) {
      state.uploadData = data;
    },
  },
  actions: {
    setUploadData({ commit }, data) {
      commit('setUploadData', data);
    },
  },
  getters: {
    getUploadData: (state) => state.uploadData,
  },
});

import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
// import Borrow from '../views/Borrow.vue';
import Return from '../views/Return.vue';
import TransactionHistory from '../components/TransactionHistory.vue';
import MyTransactions from '../views/MyTransactions.vue';
import BorrowerRegistration from '../components/BorrowerRegistration.vue';

const routes = [
  { path: '/', component: Home, props: r => ({ canBorrow: true }) },
  // { path: '/borrow', component: Borrow },
  { path: '/return', component: Return },
  { path: '/my-transactions', component: MyTransactions },
  { path: '/transactions', component: TransactionHistory },
  { path: '/add-borrower', component: BorrowerRegistration },
  // {
  //   path: '/borrow/:bookId',
  //   name: 'BorrowBookForm',
  //   component: () => import('../components/BorrowBookForm.vue')
  // }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
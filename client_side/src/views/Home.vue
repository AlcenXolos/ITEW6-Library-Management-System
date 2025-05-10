<template>
  <BookList :canBorrow="canBorrow" />
</template>

<script>
import BookList from '../components/Booklist.vue';

export default {
  props: ['canBorrow'],
  components: { BookList }
};
</script>
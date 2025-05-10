<script setup lang="ts">

const props = defineProps<{
    message: string,
    id: any 
}>();

const emit = defineEmits(['alertDismissed'])

const onClick = () => emit("alertDismissed", props.id)

</script>

<template>
    <aside class="error-card">
        {{ props.message }}
        <br />
        <button @click="onClick">Dismiss</button>
    </aside>
</template>

<style scoped>
.error-card {
    border: 1px solid #FF0000;
    box-shadow: 0 4px 8px hsl(0, 100%, 50%);
    padding-bottom: 0.5rem;
}

button {
    padding: 4px;
    float: right;
}
</style>

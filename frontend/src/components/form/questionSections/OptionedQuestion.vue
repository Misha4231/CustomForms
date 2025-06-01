<script setup lang="ts">
import { createApolloClient } from '@/services/graphQL';
import { gql } from '@apollo/client/core';
import { defineProps, onMounted, reactive, ref } from 'vue';
// ----------- WORKS FOR BOTH RADIO AND CHECKBOX INPUTs
const props = defineProps<{
  data: { isRequired: boolean },
  sectionId: string,
  isEditable: boolean,
  questionType: "RADIO" | "CHECKBOX", // type is passed in parent component with computed hook
  updateContent: (sectionId: number, data: any) => void,
  changeAnswer: (sectionId: number, data: any) => void
}>();

const questions = reactive<{text: string, id: string}[]>([]);
onMounted(async () => {
  const client = createApolloClient();
  const response = await client.query({
    query: gql`
      query options($sectionId: ID!) {
        sectionOptions(sectionId: $sectionId) {
          text
          id
        }
      }
    `,
    variables: {
      sectionId: props.sectionId
    }
  });

  const options = JSON.parse(JSON.stringify(response.data.sectionOptions));
  questions.splice(0, questions.length, ...options);
});

// Watch question option updates and push them to parent
function handleUpdate() {
  props.updateContent(parseInt(props.sectionId), {
    question: {
      answerType: props.questionType.toLowerCase(), // 'radio' or 'checkbox'
      options: questions.map(q => ({ text: q.text })) // Send only the necessary field
    }
  });
};

function addOptionHandler() {
  const newOption = {text: '', id: questions.length > 0 ? String(parseInt(questions[questions.length - 1].id) + 1) : '1'};

  questions.push(newOption);
}
function removeOptionHandler(id: string) {
  const filtered = questions.filter((q) => q.id != id);
  questions.splice(0, questions.length, ...filtered);
  handleUpdate();
}

const currentOptions = ref<number[]>([]);
function handleChooseOption(event: Event) {
  const input = event.target as HTMLInputElement;
  const optionId = parseInt(input.value);

  if (props.questionType == 'RADIO') {
    props.changeAnswer(parseInt(props.sectionId), {option: optionId});
  } else {
    if (input.checked) {
      if (!currentOptions.value.includes(optionId)) {
        currentOptions.value.push(optionId);
      }
    } else {
      currentOptions.value = currentOptions.value.filter(id => id != optionId);
    }

    props.changeAnswer(parseInt(props.sectionId), {options: currentOptions.value});
  }
}
</script>

<template>
    <div class="w-75">
        <div class="form-check d-flex align-items-center mb-2" v-for="question in questions" :key="question.id">
          <input @change="handleChooseOption" :value="question.id" :name="'option' + sectionId" class="form-check-input me-2" :type="questionType == 'RADIO' ? 'radio' : 'checkbox'" :id="'optionChoice' + sectionId + question.id" :disabled="isEditable">
          
          <label v-if="!isEditable" class="form-check-label" :for="'optionChoice' + sectionId + question.id">{{ question.text }}</label>
          <input v-else type="text" class="form-control w-50" v-model="question.text" @change="handleUpdate">

          <button v-if="isEditable" type="button" class="btn btn-danger ms-2" @click="() => removeOptionHandler(question.id)">
            <img src="/icons8-delete-48.png" width="20" alt="-">
          </button>
        </div>
        <button v-if="isEditable" type="button" class="btn btn-success mt-2" @click="addOptionHandler">
          <img src="/icons8-add-100.png" width="30" alt="+">
        </button>
    </div>
</template>
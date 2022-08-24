from omegaconf import OmegaConf


class TestExportmT5Config:
    def test_export_mt5_config(self):
        conf = OmegaConf.load("conf/export/mt5.yaml")
        s = """
        run:
          name: export_${.model_train_name}
          time_limit: "2:00:00"
          model_train_name: "mt5_390m"
          dependency: "singleton"
          task_name: "xnli"
          fine_tuning_results_dir: ${base_results_dir}/${.model_train_name}/${.task_name}
          config_summary: tp${export.model.tensor_model_parallel_size}_pp${export.triton_deployment.pipeline_model_parallel_size}_${export.model.weight_data_type}_${export.triton_deployment.data_type}
          results_dir: ${base_results_dir}/${.model_train_name}/${.task_name}_export_${.config_summary}
          model_type: "mt5"
        
        model:
          checkpoint_path: ${export.run.fine_tuning_results_dir}/checkpoints/megatron_mt5_glue_xnli.nemo
          # FT checkpoint will be saved in ${.triton_model_dir}/1/${.tensor_model_parallel_size}-gpu
          tensor_model_parallel_size: 8
          weight_data_type: fp16   # fp32|fp16
          processes: 16
          load_checkpoints_to_cpu: False
        
        triton_deployment:
          triton_model_dir: ${export.run.results_dir}/model_repo/${export.run.model_train_name}
          max_batch_size: 1
          pipeline_model_parallel_size: 1
          int8_mode: False
          enable_custom_all_reduce: False
          data_type: fp16  # fp32|fp16|bf16
        
        accuracy:
          enabled: True  # enable accuracy test
          ntasks_per_node: 8  # usually should be number of available gpus per node
          test_data: ${data_dir}/glue_data/xnli/xnli.test.tsv
          output_path: ${export.run.results_dir}/eval_output.json
          batch_size: 64
          max_output_len: 512
          runtime:
            beam_width: 1
            sampling_top_k: 1
            sampling_top_p: 0

        benchmark:
          input_len: 60
          output_len: 20
          batch_sizes: [1, 2, 4, 8, 16, 32, 64, 128, 256]
          triton_wait_time_s: 300
          vocab_size: 250112
        """
        expected = OmegaConf.create(s)
        assert (
                expected == conf
        ), f"conf/export/mt5.yaml must be set to {expected} but it currently is {conf}."


class TestExportT5Config:
    def test_export_t5_config(self):
        conf = OmegaConf.load("conf/export/t5.yaml")
        s = """
        run:
          name: export_${.model_train_name}
          time_limit: "2:00:00"
          model_train_name: "t5_220m"
          dependency: "singleton"
          task_name: "mnli"
          fine_tuning_results_dir: ${base_results_dir}/${.model_train_name}/${.task_name}
          config_summary: tp${export.model.tensor_model_parallel_size}_pp${export.triton_deployment.pipeline_model_parallel_size}_${export.model.weight_data_type}_${export.triton_deployment.data_type}
          results_dir: ${base_results_dir}/${.model_train_name}/${.task_name}_export_${.config_summary}
          model_type: "t5"

        model:
          checkpoint_path: ${export.run.fine_tuning_results_dir}/checkpoints/megatron_t5_glue.nemo
          # FT checkpoint will be saved in ${.triton_model_dir}/1/${.tensor_model_parallel_size}-gpu
          tensor_model_parallel_size: 8
          weight_data_type: fp16   # fp32|fp16
          processes: 16
          load_checkpoints_to_cpu: False

        triton_deployment:
          triton_model_dir: ${export.run.results_dir}/model_repo/${export.run.model_train_name}
          max_batch_size: 1
          pipeline_model_parallel_size: 1
          int8_mode: False
          enable_custom_all_reduce: False
          data_type: fp16  # fp32|fp16|bf16

        accuracy:
          enabled: True  # enable accuracy test
          ntasks_per_node: 8  # usually should be number of available gpus per node
          test_data: ${data_dir}/glue_data/mnli/dev_matched.tsv
          output_path: ${export.run.results_dir}/eval_output.json
          batch_size: 64
          max_output_len: 512
          runtime:
            beam_width: 1
            sampling_top_k: 1
            sampling_top_p: 0

        benchmark:
          input_len: 60
          output_len: 20
          batch_sizes: [1, 2, 4, 8, 16, 32, 64, 128, 256]
          triton_wait_time_s: 300
          vocab_size: 29184
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/export/t5.yaml must be set to {expected} but it currently is {conf}."


class TestExportGPT3Config:
    def test_export_gpt3_config(self):
        conf = OmegaConf.load("conf/export/gpt3.yaml")
        s = """
        run:
          name: export_${.model_train_name}
          time_limit: "2:00:00"
          model_train_name: "gpt3_5b"
          dependency: "singleton"
          training_dir: ${base_results_dir}/${.model_train_name}
          config_summary: tp${export.model.tensor_model_parallel_size}_pp${export.triton_deployment.pipeline_model_parallel_size}_${export.model.weight_data_type}_${export.triton_deployment.data_type}
          results_dir: ${base_results_dir}/${.model_train_name}/export_${.config_summary}
          model_type: "gpt3"
        
        model:
          checkpoint_path: ${export.run.training_dir}/checkpoints
          # FT checkpoint will be saved in ${.triton_model_dir}/1/${.tensor_model_parallel_size}-gpu
          tensor_model_parallel_size: 8
          weight_data_type: fp16   # fp32|fp16
          processes: 16
          load_checkpoints_to_cpu: False
        
        triton_deployment:
          triton_model_dir: ${export.run.results_dir}/model_repo/${export.run.model_train_name}
          max_batch_size: 1
          pipeline_model_parallel_size: 1
          int8_mode: False
          enable_custom_all_reduce: False
          data_type: fp16  # fp32|fp16|bf16
        
        accuracy:
          enabled: True  # enable accuracy test
          ntasks_per_node: 8  # usually should be number of available gpus per node
          runtime_config_ini_path: ${export.run.results_dir}/ft_runtime.ini
          test_data: ${export.run.results_dir}/lambada_test.jsonl
          output_path: ${export.run.results_dir}/eval_output.json
          batch_size: 64
          runtime:
            max_seq_len: 512
            beam_width: 1
            sampling_top_k: 1
            sampling_top_p: 0

        benchmark:
          input_len: 60
          output_len: 20
          batch_sizes: [1, 2, 4, 8, 16, 32, 64, 128, 256]
          triton_wait_time_s: 300
          vocab_size: 51200
        """
        expected = OmegaConf.create(s)
        assert (
            expected == conf
        ), f"conf/export/gpt3.yaml must be set to {expected} but it currently is {conf}."


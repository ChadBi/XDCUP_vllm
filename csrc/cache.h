#pragma once

#include <torch/extension.h>

#include <map>
#include <vector>

void swap_blocks(
  torch::Tensor& src,
  torch::Tensor& dst,
  const std::map<int64_t, int64_t>& block_mapping);

void copy_blocks(
  std::vector<torch::Tensor>& key_caches,
  std::vector<torch::Tensor>& value_caches,
  const std::map<int64_t, std::vector<int64_t>>& block_mapping);

void reshape_and_cache(
  torch::Tensor& key,
  torch::Tensor& value,
  torch::Tensor& key_cache,
  torch::Tensor& value_cache,
  torch::Tensor& slot_mapping,
  const std::string& kv_cache_dtype,
  const float k_scale = 1.0f,
  const float k_zp = 0.0f,
  const float v_scale = 1.0f,
  const float v_zp = 0.0f);

// Just for unittest
void convert_fp8_e5m2(
  torch::Tensor& src_cache,
  torch::Tensor& dst_cache);

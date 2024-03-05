<template>
  <div id="app">
    <ng-form-design ref="formDesign" disabled="true" />
    <ng-form-build ref="formBuild" disabled="true" />
  </div>
</template>

<script>
import NgFormElementPlus from "ng-form-elementplus";
import "ng-form-elementplus/lib/style.css";
import ConvertJsonToTable from "../components/json-to-table";
import html2canvas from "html2canvas";
import store from "@/store";
import { saveGraph, getAGraph } from "../api/graph";
import { ElMessage } from "element-plus";

export default {
  components: {
    // 注册插件提供的组件，如果需要的话
    NgFormElementPlus,
    ConvertJsonToTable,
  },
  data() {
    return {
      models: {},
      formTemplate: {},
      showPreview: false,
      selectBox: "",
      pageWidth: 320,
      pageHeight: 0,
      isSelfOptionShow: false,
      inputHeightBox: "",
      inputWidthBox: "",
      mutipleIcon: "",
      commitButton: "",

      graphid: "",
      projectid: "",
      currentGraph: {
        content: "",
      },
      graphFile: "",
    };
  },
  methods: {
    base64ToFile(base64, fileName) {
      let arr = base64.split(",");
      let mime = arr[0].match(/:(.\*?);/)[1];
      console.log(mime);
      let bstr = atob(arr[1]);
      let n = bstr.length;
      let u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], fileName, { type: mime });
    },
    saveJson() {
      console.log(this.pageWidth);
      var promise = saveGraph(
        this.graphid,
        this.projectid,
        JSON.stringify(this.$refs.formDesign.getModel()),
        this.pageWidth,
        this.graphFile
      );
      promise.then((result) => {
        this.MessageCatch(result, true);
      });
    },
    GetAGraph() {
      var promise = getAGraph(this.graphid, this.projectid);
      promise.then((result) => {
        if (this.MessageCatch(result, false)) {
          this.pageWidth = result.data.width;
          if (result.data.content === "") {
          } else {
            this.currentGraph.content = JSON.parse(result.data.content);
            this.$refs.formDesign.initModel(this.currentGraph.content);
          }
        }
      });
    },
    MessageCatch(data, opcode) {
      if (data.code != 0) {
        ElMessage({
          message: data.msg,
          grouping: true,
          type: "error",
        });
        return false;
      }
      if (opcode == true && data.code == 0) {
        ElMessage({
          message: data.msg,
          grouping: true,
          type: "success",
        });
      }
      return true;
    },
    getPicture() {
      var ele = document.querySelector(".el-dialog__body");
      if (ele) {
        var that = this;
        html2canvas(ele)
          .then(function (canvas) {
            const imgUrl = canvas.toDataURL("image/jpeg", 1.0);
            const link = document.createElement("a");
            console.log(imgUrl);
            link.href = imgUrl;
            console.log(imgUrl);

            let arr = imgUrl.split(",");
            let bstr = atob(arr[1]);
            let n = bstr.length;
            let u8arr = new Uint8Array(n);
            while (n--) {
              u8arr[n] = bstr.charCodeAt(n);
            }
            that.graphFile = new File([u8arr], "text", { type: "image/jpg" });
            that.saveJson();
            var str = that.selectBox.value;
            link.download = "exported_image." + str; // Set the download filename
            link.click();
          })
          .catch(function (error) {
            console.error("html2canvas error:", error);
          });
      } else {
        console.error("Element not found");
      }
    },
    test1() {
      this.$refs.formDesign.getModel();
    },
    test2() {
      this.$refs.formDesign.initModel();
    },
    hideButton() {
      this.inputHeightBox.style.display = "none";
      this.inputWidthBox.style.display = "none";
      this.mutipleIcon.style.display = "none";
      this.commitButton.style.display = "none";
    },
    createSelectBox() {
      var selectElement = document.createElement("select");
      var option1 = document.createElement("option");
      option1.value = "jpg";
      option1.text = "jpg";
      var option2 = document.createElement("option");
      option2.value = "png";
      option2.text = "png";
      selectElement.appendChild(option1);
      selectElement.appendChild(option2);
      selectElement.classList.add("custom-select");
      return selectElement;
    },
    createSelecChangetBox() {
      var selectElement = document.createElement("select");
      var option1 = document.createElement("option");
      option1.value = "page";
      option1.text = "网页 1440×1204";
      var option2 = document.createElement("option");
      option2.value = "ipad";
      option2.text = "ipad mini 1024×768";
      var option3 = document.createElement("option");
      option3.value = "phone";
      option3.text = "iPhone 13 Pro Max 428×926";
      var option4 = document.createElement("option");
      option4.value = "self";
      option4.text = "自定义";
      selectElement.appendChild(option1);
      selectElement.appendChild(option2);
      selectElement.appendChild(option3);
      selectElement.appendChild(option4);
      selectElement.classList.add("Change-select");
      var that = this;
      selectElement.addEventListener("change", () => {
        var eleAsidRight = document.querySelector(
          "#app > section > main > section > aside.el-aside.properties-panel"
        );
        var eleAsidLeft = document.querySelector(
          "#app > section > main > section > aside.el-aside.item-panel"
        );
        if (selectElement.value == "page") {
          eleAsidRight.style = "width : 320px";
          eleAsidLeft.style = "width : 320px";
          that.pageWidth = 320;
          that.hideButton();
        } else if (selectElement.value == "ipad") {
          eleAsidRight.style = "width : 220px";
          eleAsidLeft.style = "width : 220px";
          that.pageWidth = 220;
          that.hideButton();
        } else if (selectElement.value == "phone") {
          eleAsidRight.style = "width : 480px";
          eleAsidLeft.style = "width : 480px";
          that.pageWidth = 480;
          that.hideButton();
        } else if (selectElement.value == "self") {
          this.inputHeightBox.style.display = "flex";
          this.inputWidthBox.style.display = "flex";
          this.mutipleIcon.style.display = "flex";
          this.commitButton.style.display = "flex";
        }
      });
      return selectElement;
    },
    createSelectModel() {
      var selectElement = document.createElement("select");
      var option1 = document.createElement("option");
      option1.value = 1;
      option1.text = "空白原型";
      var option2 = document.createElement("option");
      option2.value = 2;
      option2.text = "PC 学术中心";
      var option3 = document.createElement("option");
      option3.value = 3;
      option3.text = "移动 商城首页";
      selectElement.appendChild(option1);
      selectElement.appendChild(option2);
      selectElement.appendChild(option3);
      selectElement.classList.add("Change-select-Model");
      var that = this;
      selectElement.addEventListener("change", () => {
        if (selectElement.value == 1) {
          var model = `{
	"list": [],
	"config": {
		"labelPosition": "left",
		"labelWidth": 100,
		"size": "default",
		"outputHidden": true,
		"hideRequiredMark": false,
		"syncLabelRequired": false,
		"customStyle": ""
	}
}`;
          this.$refs.formDesign.initModel(JSON.parse(model));
          this.pageWidth = 320
          return;
        } else if (selectElement.value == 2) {
          that.pageWidth = 320;
          var model = `{
	"list": [
		{
			"type": "input",
			"options": {
				"type": "text",
				"placeholder": "请输入",
				"clearable": false,
				"hidden": false,
				"disabled": false
			},
			"label": "输入关键",
			"labelWidth": -1,
			"width": "100%",
			"span": 24,
			"model": "input_16936650638520",
			"key": "input_16936650638520",
			"rules": [
				{
					"required": false,
					"message": "必填项",
					"trigger": [
						"blur"
					]
				}
			]
		},
		{
			"type": "grid",
			"layout": true,
			"options": {
				"gutter": 0,
				"hidden": false,
				"disabled": false
			},
			"label": "栅格布局",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"columns": [
				{
					"span": 12,
					"list": [
						{
							"type": "grid",
							"layout": true,
							"options": {
								"gutter": 0,
								"hidden": false,
								"disabled": false
							},
							"label": "栅格布局",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"columns": [
								{
									"span": 12,
									"list": [
										{
											"type": "select",
											"options": {
												"placeholder": "请输入",
												"dynamic": 0,
												"options": [
													{
														"value": "1",
														"label": "下拉框1"
													},
													{
														"value": "2",
														"label": "下拉框2"
													}
												],
												"methodType": "get",
												"multiple": false,
												"showSearch": false,
												"clearable": false,
												"hidden": false,
												"disabled": false,
												"linkage": false,
												"linkData": []
											},
											"label": "地区",
											"labelWidth": -1,
											"width": "100%",
											"span": 24,
											"model": "select_1693665508216",
											"key": "select_1693665508216",
											"rules": [
												{
													"required": false,
													"message": "必填项",
													"trigger": [
														"blur"
													]
												}
											]
										}
									]
								},
								{
									"span": 12,
									"list": [
										{
											"type": "select",
											"options": {
												"placeholder": "请输入",
												"dynamic": 0,
												"options": [
													{
														"value": "1",
														"label": "下拉框1"
													},
													{
														"value": "2",
														"label": "下拉框2"
													}
												],
												"methodType": "get",
												"multiple": false,
												"showSearch": false,
												"clearable": false,
												"hidden": false,
												"disabled": false,
												"linkage": false,
												"linkData": []
											},
											"label": "语言",
											"labelWidth": -1,
											"width": "100%",
											"span": 24,
											"model": "select_1693665509667",
											"key": "select_1693665509667",
											"rules": [
												{
													"required": false,
													"message": "必填项",
													"trigger": [
														"blur"
													]
												}
											]
										}
									]
								}
							],
							"key": "grid_1693665445459",
							"model": "grid_1693665445459"
						}
					]
				},
				{
					"span": 12,
					"list": [
						{
							"type": "grid",
							"layout": true,
							"options": {
								"gutter": 0,
								"hidden": false,
								"disabled": false
							},
							"label": "栅格布局",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"columns": [
								{
									"span": 12,
									"list": [
										{
											"type": "select",
											"options": {
												"placeholder": "请输入",
												"dynamic": 0,
												"options": [
													{
														"value": "1",
														"label": "下拉框1"
													},
													{
														"value": "2",
														"label": "下拉框2"
													}
												],
												"methodType": "get",
												"multiple": false,
												"showSearch": false,
												"clearable": false,
												"hidden": false,
												"disabled": false,
												"linkage": false,
												"linkData": []
											},
											"label": "类型",
											"labelWidth": -1,
											"width": "100%",
											"span": 24,
											"model": "select_1693665515741",
											"key": "select_1693665515741",
											"rules": [
												{
													"required": false,
													"message": "必填项",
													"trigger": [
														"blur"
													]
												}
											]
										}
									]
								},
								{
									"span": 12,
									"list": [
										{
											"type": "daterange",
											"options": {
												"dateType": "date",
												"format": "YYYY-MM-DD",
												"rangeStartPlaceholder": "请输入",
												"rangeEndPlaceholder": "请输入",
												"clearable": false,
												"hidden": false,
												"disabled": false
											},
											"label": "日期区间",
											"labelWidth": -1,
											"width": "100%",
											"span": 24,
											"model": "daterange_1693665513934",
											"key": "daterange_1693665513934",
											"rules": [
												{
													"required": false,
													"message": "必填项",
													"trigger": [
														"blur"
													]
												}
											]
										}
									]
								}
							],
							"key": "grid_1693665450015",
							"model": "grid_1693665450015"
						}
					]
				}
			],
			"key": "grid_16936654295962",
			"model": "grid_16936654295962"
		},
		{
			"type": "controller",
			"layout": true,
			"options": {
				"bordered": false,
				"add": true,
				"copy": true,
				"remove": true,
				"hidden": false,
				"disabled": false
			},
			"label": "容器",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"key": "controller_16936655382231",
			"model": "controller_16936655382231",
			"list": [
				{
					"type": "table",
					"layout": true,
					"options": {
						"bordered": false,
						"bright": true,
						"small": true,
						"hidden": false
					},
					"label": "表格布局",
					"labelWidth": 0,
					"width": "100%",
					"span": 24,
					"key": "table_1693665543545",
					"model": "table_1693665543545",
					"trs": [
						{
							"tds": [
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								},
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								}
							]
						},
						{
							"tds": [
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								},
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								}
							]
						}
					]
				},
				{
					"type": "table",
					"layout": true,
					"options": {
						"bordered": false,
						"bright": true,
						"small": true,
						"hidden": false
					},
					"label": "表格布局",
					"labelWidth": 0,
					"width": "100%",
					"span": 24,
					"key": "table_1693665546303",
					"model": "table_1693665546303",
					"trs": [
						{
							"tds": [
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								},
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								}
							]
						},
						{
							"tds": [
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								},
								{
									"colspan": 1,
									"rowspan": 1,
									"list": []
								}
							]
						}
					]
				}
			]
		}
	],
	"config": {
		"labelPosition": "left",
		"labelWidth": 100,
		"size": "default",
		"outputHidden": true,
		"hideRequiredMark": false,
		"syncLabelRequired": false,
		"customStyle": ""
	}
}`;
          this.$refs.formDesign.initModel(JSON.parse(model));
        } else if (selectElement.value == 3) {
          that.pageWidth = 480;
          var model = `{
	"list": [
		{
			"type": "input",
			"options": {
				"type": "text",
				"placeholder": "请输入",
				"clearable": false,
				"hidden": false,
				"disabled": false
			},
			"label": "输入框",
			"labelWidth": -1,
			"width": "100%",
			"span": 24,
			"model": "input_16936658818170",
			"key": "input_16936658818170",
			"rules": [
				{
					"required": false,
					"message": "必填项",
					"trigger": [
						"blur"
					]
				}
			]
		},
		{
			"type": "controller",
			"layout": true,
			"options": {
				"bordered": true,
				"add": true,
				"copy": true,
				"remove": true,
				"hidden": false,
				"disabled": false
			},
			"label": "容器",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"key": "controller_16936658966491",
			"model": "controller_16936658966491",
			"list": [
				{
					"type": "grid",
					"layout": true,
					"options": {
						"gutter": 0,
						"hidden": false,
						"disabled": false
					},
					"label": "栅格布局",
					"labelWidth": 0,
					"width": "100%",
					"span": 24,
					"columns": [
						{
							"span": 12,
							"list": [
								{
									"type": "grid",
									"layout": true,
									"options": {
										"gutter": 0,
										"hidden": false,
										"disabled": false
									},
									"label": "栅格布局",
									"labelWidth": 0,
									"width": "100%",
									"span": 24,
									"columns": [
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665934823",
													"key": "uploadImg_1693665934823",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										},
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665948530",
													"key": "uploadImg_1693665948530",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										}
									],
									"key": "grid_1693665900278",
									"model": "grid_1693665900278"
								}
							]
						},
						{
							"span": 12,
							"list": [
								{
									"type": "grid",
									"layout": true,
									"options": {
										"gutter": 0,
										"hidden": false,
										"disabled": false
									},
									"label": "栅格布局",
									"labelWidth": 0,
									"width": "100%",
									"span": 24,
									"columns": [
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665961418",
													"key": "uploadImg_1693665961418",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										},
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665965360",
													"key": "uploadImg_1693665965360",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										}
									],
									"key": "grid_1693665901723",
									"model": "grid_1693665901723"
								}
							]
						}
					],
					"key": "grid_1693665899191",
					"model": "grid_1693665899191"
				},
				{
					"type": "grid",
					"layout": true,
					"options": {
						"gutter": 0,
						"hidden": false,
						"disabled": false
					},
					"label": "栅格布局",
					"labelWidth": 0,
					"width": "100%",
					"span": 24,
					"columns": [
						{
							"span": 12,
							"list": [
								{
									"type": "grid",
									"layout": true,
									"options": {
										"gutter": 0,
										"hidden": false,
										"disabled": false
									},
									"label": "栅格布局",
									"labelWidth": 0,
									"width": "100%",
									"span": 24,
									"columns": [
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665934823",
													"key": "uploadImg_1693665934823",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										},
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665948530",
													"key": "uploadImg_1693665948530",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										}
									],
									"key": "grid_1693665900278",
									"model": "grid_1693665900278"
								}
							]
						},
						{
							"span": 12,
							"list": [
								{
									"type": "grid",
									"layout": true,
									"options": {
										"gutter": 0,
										"hidden": false,
										"disabled": false
									},
									"label": "栅格布局",
									"labelWidth": 0,
									"width": "100%",
									"span": 24,
									"columns": [
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665961418",
													"key": "uploadImg_1693665961418",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										},
										{
											"span": 12,
											"list": [
												{
													"type": "uploadImg",
													"options": {
														"listType": "picture-card",
														"limitSize": 10,
														"defaultValue": [],
														"multiple": false,
														"limit": 3,
														"hidden": false,
														"disabled": false,
														"headers": []
													},
													"label": "上传图片",
													"labelWidth": 0,
													"width": "100%",
													"span": 24,
													"model": "uploadImg_1693665965360",
													"key": "uploadImg_1693665965360",
													"rules": [
														{
															"required": false,
															"message": "必填项",
															"trigger": [
																"blur"
															]
														}
													]
												}
											]
										}
									],
									"key": "grid_1693665901723",
									"model": "grid_1693665901723"
								}
							]
						}
					],
					"key": "grid_1693665969637",
					"model": "grid_1693665969637"
				}
			]
		},
		{
			"type": "grid",
			"layout": true,
			"options": {
				"gutter": 0,
				"hidden": false,
				"disabled": false
			},
			"label": "栅格布局",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"columns": [
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666005771",
							"key": "uploadImg_1693666005771",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				},
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666008669",
							"key": "uploadImg_1693666008669",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				}
			],
			"key": "grid_16936659905762",
			"model": "grid_16936659905762"
		},
		{
			"type": "grid",
			"layout": true,
			"options": {
				"gutter": 0,
				"hidden": false,
				"disabled": false
			},
			"label": "栅格布局",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"columns": [
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666005771",
							"key": "uploadImg_1693666005771",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				},
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666008669",
							"key": "uploadImg_1693666008669",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				}
			],
			"key": "grid_1693666036322",
			"model": "grid_1693666036322"
		},
		{
			"type": "grid",
			"layout": true,
			"options": {
				"gutter": 0,
				"hidden": false,
				"disabled": false
			},
			"label": "栅格布局",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"columns": [
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666005771",
							"key": "uploadImg_1693666005771",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				},
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666008669",
							"key": "uploadImg_1693666008669",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				}
			],
			"key": "grid_1693666035849",
			"model": "grid_1693666035849"
		},
		{
			"type": "grid",
			"layout": true,
			"options": {
				"gutter": 0,
				"hidden": false,
				"disabled": false
			},
			"label": "栅格布局",
			"labelWidth": 0,
			"width": "100%",
			"span": 24,
			"columns": [
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666005771",
							"key": "uploadImg_1693666005771",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				},
				{
					"span": 12,
					"list": [
						{
							"type": "uploadImg",
							"options": {
								"listType": "picture-card",
								"limitSize": 10,
								"defaultValue": [],
								"multiple": false,
								"limit": 3,
								"hidden": false,
								"disabled": false,
								"headers": []
							},
							"label": "上传图片",
							"labelWidth": 0,
							"width": "100%",
							"span": 24,
							"model": "uploadImg_1693666008669",
							"key": "uploadImg_1693666008669",
							"rules": [
								{
									"required": false,
									"message": "必填项",
									"trigger": [
										"blur"
									]
								}
							]
						}
					]
				}
			],
			"key": "grid_1693666034778",
			"model": "grid_1693666034778"
		}
	],
	"config": {
		"labelPosition": "left",
		"labelWidth": 100,
		"size": "default",
		"outputHidden": true,
		"hideRequiredMark": false,
		"syncLabelRequired": false,
		"customStyle": ""
	}
}`;
          this.$refs.formDesign.initModel(JSON.parse(model));
          console.log(model);
        }
      });
      return selectElement;
    },
    createInputHeight() {
      var selectElement = document.createElement("input");
      selectElement.classList.add("inputHeight");
      return selectElement;
    },
    createInputWidth() {
      var selectElement = document.createElement("input");
      selectElement.classList.add("inputWidth");
      return selectElement;
    },
    init() {
      this.GetAGraph();
      var elementToDelete = document.querySelector(
        "#app > section > header > div > div > div:nth-child(1)"
      );
      if (elementToDelete) {
        // 删除元素
        elementToDelete.remove();
      } else {
        console.log("未找到要删除的元素。");
      }
      var buttonSpan = document.querySelector(
        "#app > section > header > div > div > div:nth-child(2) > span"
      );
      var saveButton = document.querySelector(
        "#app > section > header > div > div > div:nth-child(2) > span > button:nth-child(3)"
      );
      var tempButton = saveButton.cloneNode(true); // Perform a deep clone
      tempButton.childNodes[1].textContent = "保存";
      buttonSpan.appendChild(tempButton);
      console.log(saveButton);
      tempButton.addEventListener("click", () => {
        this.saveJson();
      });
      var changeWitdhSpan = document.querySelector(
        "#app > section > header > div > div > div:nth-child(1)"
      );
      changeWitdhSpan.style = "height : 40px;";
      var changWidBox = this.createSelecChangetBox();
      var changeModelBox = this.createSelectModel();
      changeWitdhSpan.appendChild(changWidBox);
      changeWitdhSpan.appendChild(changeModelBox);
      this.inputHeightBox = this.createInputHeight();
      this.inputWidthBox = this.createInputWidth();
      this.mutipleIcon = document.createElement("span");
      this.commitButton = document.createElement("button");
      this.commitButton.classList.add("commitButton");
      this.mutipleIcon.classList.add("mutipleIcon");
      this.mutipleIcon.textContent = "×";
      this.commitButton.textContent = "确定";
      var that = this;
      this.commitButton.addEventListener("click", () => {
        var eleAsidRight = document.querySelector(
          "#app > section > main > section > aside.el-aside.properties-panel"
        );
        var eleAsidLeft = document.querySelector(
          "#app > section > main > section > aside.el-aside.item-panel"
        );
        that.pageWidth = 0.77 * that.inputWidthBox.value;
        eleAsidRight.style.width = that.pageWidth + "px";
        eleAsidLeft.style.width = that.pageWidth + "px";
      });
      changeWitdhSpan.appendChild(this.inputHeightBox);
      changeWitdhSpan.appendChild(this.inputWidthBox);
      changeWitdhSpan.appendChild(this.mutipleIcon);
      changeWitdhSpan.appendChild(this.commitButton);
      var eleThingContainer = document.querySelector(
        ".el-main.center-panel.form-main"
      );
      console.log(eleThingContainer.style.width);
      var ele1 = document.querySelector(
        "#app > section > header > div > div > div:nth-child(2) > span > button:nth-child(2)"
      );

      ele1.addEventListener("click", () => {
        this.showPreview = true;
        var ele;
        // var temp = document.querySelector(
        //   "body > div:nth-child(20) > div > div > header > button"
        // );
        var temp;
        var i;
        // for(i=4;i<100;i++){
        //   temp=document.querySelector("body > div:nth-child("+i+")")
        //   console.log(temp)
        //   if(temp != null){
        //     break;
        //   }
        // }
        var charTemp = "body > div:nth-child(" + i + ")";
        console.log(charTemp);
        // if (temp) charTemp = "body > div:nth-child(20)";
        // else charTemp = "body > div:nth-child(4)";
        console.log(ele);
        ele = document.querySelector(".el-dialog__headerbtn");
        ele.addEventListener("click", () => {
          this.showPreview = false;
        });
        var dialog = document.querySelector(".el-dialog.design-preview");
        // var temp = document.querySelector(
        //   "body > div:nth-child(4) > div > div"
        // );
        // temp.style.width = 1440 - that.pageWidth * 2 + "px";
        dialog.style.zIndex = "9999";
        var newElButton = document.createElement("button");
        newElButton.setAttribute("type", "primary");
        newElButton.setAttribute("class", "previewButton");
        newElButton.textContent = "导出图片";
        newElButton.addEventListener("click", this.getPicture);
        newElButton.style =
          "background-color : #409EFF;border : 0;color : white;border-radius : 2px;cursor: pointer;margin-left : 10px;height:24px;font-size:6px";
        newElButton.addEventListener("mouseover", () => {
          newElButton.style.backgroundColor = "#79bbff";
        });
        newElButton.addEventListener("mouseout", () => {
          newElButton.style.backgroundColor = "#409EFF";
        });
        this.selectBox = this.createSelectBox();
        var header = document.querySelector(".dialog-footer");
        header.appendChild(newElButton);
        header.appendChild(this.selectBox);
      });
    },
  },
  mounted() {
    this.projectid = this.$route.params.projectid;
    this.graphid = this.$route.params.designid;
    if (store.state.isLogin == false) this.$router.push("/");
    this.init();
  },
  watch: {
    pageWidth: function (newVal, oldVal) {
      console.log(this.pageWidth);
      var eleAsidRight = document.querySelector(
        "#app > section > main > section > aside.el-aside.properties-panel"
      );
      var eleAsidLeft = document.querySelector(
        "#app > section > main > section > aside.el-aside.item-panel"
      );
      eleAsidRight.style.width = this.pageWidth + "px";
      eleAsidLeft.style.width = this.pageWidth + "px";
    },
  },
};
</script>

<style>
.Change-select-Model {
  position: absolute;
  display: flex;
  left: 350px;
  top: 10px;
  height: 24px;
  background-color: #409eff;
  color: white;
  border-color: #409eff;
  border-radius: 3px;
  box-shadow: 2px 2px 5px #409eff;
}
.commitButton {
  cursor: pointer;
  position: absolute;
  display: none;
  top: 9px;
  left: 1370px;
  height: 24px;
  width: 50px;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
  border: 0;
  box-shadow: 2px 2px 5px #409eff;
}
.mutipleIcon {
  position: absolute;
  display: none;
  border: 0;
  left: 1280px;
  top: 13px;
}
.inputHeight {
  position: absolute;
  display: none;
  height: 20px;
  width: 40px;
  left: 1220px;
  top: 10px;
  border-radius: 5px;
  box-shadow: 4px 4px 10px #b1b3b8;
  border: 0;
}
.inputWidth {
  position: absolute;
  display: none;
  height: 20px;
  width: 40px;
  left: 1300px;
  top: 10px;
  border-radius: 5px;
  box-shadow: 4px 4px 10px #b1b3b8;
  border: 0;
}
.custom-select {
  margin-left: 10px;
  height: 24px;
  background-color: #409eff;
  color: white;
  border: 0;
  border-radius: 3px;
}
.Change-select {
  margin-left: 10px;
  height: 24px;
  background-color: #409eff;
  color: white;
  border-color: #409eff;
  border-radius: 3px;
  margin-left: 1000px;
  margin-top: 8px;
  box-shadow: 2px 2px 5px #409eff;
}
</style>

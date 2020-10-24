/*
   * Modifica el json global para que tenga las etiquetas del project xml
   * Luego, con la libreria xml2json la vuelvo xml
   */
  function parsear_data_json(data_json){
    let xml_project = {
      "Project":{
        "@xmlns":"http://schemas.microsoft.com/project",
        "SaveVersion":14,
        "Name":data_json.text+'.xml',
        "Title":data_json.text,
        "CreationDate":parsear_fecha(new Date()),
        "LastSaved":parsear_fecha(new Date()),
        "ScheduleFromStart":1,
        "StartDate":parsear_fecha(new Date(data_json.start_date_real)),
        "FinishDate":parsear_fecha(new Date(data_json.end_date_real)),
        "FYStartDate":1,
        "CriticalSlackLimit":0,
        "CurrencyDigits":2,
        "DefaultTaskType":0,
        "DefaultFixedCostAccrual":3,
        "DefaultStandardRate":0,
        "DefaultOvertimeRate":0,
        "DurationFormat":7,
        "WorkFormat":2,
        "EditableActualCosts":0,
        "HonorConstraints":0,
        "InsertedProjectsLikeSummary":1,
        "MultipleCriticalPaths":0,
        "NewTasksEffortDriven":0,
        "NewTasksEstimated":1,        
        "SplitsInProgressTasks":1,
        "SpreadActualCost":0,
        "SpreadPercentComplete":0,
        "TaskUpdatesResource":1,
        "FiscalYearStart":0,
        "WeekStartDay":1,
        "MoveCompletedEndsBack":0,
        "MoveRemainingStartsBack":0,
        "MoveRemainingStartsForward":0,
        "MoveCompletedEndsForward":0,
        "BaselineForEarnedValue":0,
        "AutoAddNewResourcesAndTasks":1,
        "CurrentDate":parsear_fecha(new Date(data_json.start_date_real)),
        "MicrosoftProjectServerURL":1,
        "Autolink":0,
        "NewTaskStartDate":0,
        "NewTasksAreManual":1,
        "DefaultTaskEVMethod":0,
        "ProjectExternallyEdited":0,
        "ExtendedCreationDate":"1984-01-01T00:00:00",
        "ActualsInSync":0,
        "RemoveFileProperties":0,
        "AdminProject":0,
        "UpdateManuallyScheduledTasksWhenEditingLinks":1,
        "KeepTaskOnNearestWorkingTimeWhenMadeAutoScheduled":0,
        "OutlineCodes":"",
        "WBSMasks":"",
        "ExtendedAttributes":"",
        "Tasks":{"Task":[]}
      }
    }
    let cont = 1;
    let cont_id = 1;
    xml_project["Project"]["Tasks"]["Task"].push(
      get_task(
        cont_id, 
        cont_id, 
        data_json.text, 
        data_json.start_date_real, 
        data_json.end_date_real, 
        data_json.duration_real, 
        cont,
        1)
    );
    let riesgos = data_json.children;      
    wbs_riesgos = 1;
    for(let i = 0; i < riesgos.length; i++){      
      cont_id++;
      xml_project["Project"]["Tasks"]["Task"].push(
      get_task(
        cont_id, 
        cont_id, 
        riesgos[i].text, 
        riesgos[i].start_date_real, 
        riesgos[i].end_date_real, 
        riesgos[i].duration_real, 
        cont+'.'+wbs_riesgos,
        2)
      );
      let actividades = riesgos[i].children;      
      wbs_actividades = 1;  
      for(let j = 0; j < actividades.length; j++){        
        cont_id++;
        xml_project["Project"]["Tasks"]["Task"].push(
        get_task(
          cont_id, 
          cont_id, 
          actividades[j].text, 
          actividades[j].start_date_real, 
          actividades[j].end_date_real, 
          actividades[j].duration_real, 
          cont+'.'+wbs_riesgos+'.'+wbs_actividades,
          3)
        );
        let tareas = actividades[j].children;  
        wbs_tareas = 1;        
        for(let k = 0; k < tareas.length; k++){          
          cont_id++;
          console.log("fecha",tareas[k]);
          xml_project["Project"]["Tasks"]["Task"].push(
          get_task(
            cont_id, 
            cont_id, 
            tareas[k].text, 
            tareas[k].start_date_real, 
            tareas[k].end_date_real, 
            tareas[k].duration_real, 
            cont+'.'+wbs_riesgos+'.'+wbs_actividades+'.'+wbs_tareas,
            4)
          );
          wbs_tareas++;
        }
        wbs_actividades++;          
      }      
      wbs_riesgos++;
    } 
    return xml_project;
  }

function parsear_fecha(now){    
 return moment(now).format('YYYY-MM-DDThh:mm:ss');
}

function parsear_duration(duracion_dias){
  let horas = Math.round(duracion_dias*24);    
  //return 'PT1H0M0S';
  return 'PT'+horas+'H0M0S';
}

function get_task(uid, id, name, start_date, end_date, duration, wbs,OutlineLevel){
  return {
      "UID":uid,
      "ID":id,
      "Name":name,
      "Active":1,
      "Manual":1,
      "Type":1,
      "IsNull":0,
      "CreateDate":parsear_fecha(new Date()),
      "WBS":wbs,
      "OutlineNumber":wbs,
      "OutlineLevel":OutlineLevel,
      "Priority":500,
      "Start":parsear_fecha(new Date(start_date)),
      "Finish":parsear_fecha(new Date(end_date)),
      "Duration":parsear_duration(duration),
      "ManualStart":parsear_fecha(new Date(start_date)),
      "ManualFinish":parsear_fecha(new Date(end_date)),
      "ManualDuration":parsear_duration(duration),
      "DurationFormat":7
  };
}



